from .memory import Memory
from .models import State
from .planner import deterministic_plan,parse_plan
from .tools import TOOLS,RISK

class Agent:
    def __init__(self,workspace=".",memory_path="agent.db",llm=None): self.workspace=workspace; self.memory=Memory(memory_path); self.llm=llm
    def make_plan(self,goal):
        if not self.llm:return deterministic_plan(goal)
        prompt='Return ONLY JSON with steps. Allowed tools: '+', '.join(TOOLS)+'\nGoal: '+goal
        return parse_plan(goal,self.llm.chat([{"role":"system","content":"You are a cautious software engineering planner."},{"role":"user","content":prompt}]))
    def run(self,goal,approve=False):
        plan=self.make_plan(goal); trace=[]; events=[]; state=State.EXECUTING
        self.memory.add(State.PLANNING.value,"plan","plan created",{"steps":[s.tool for s in plan.steps]})
        for step in plan.steps:
            risk=RISK.get(step.tool,"high")
            if risk!="low" and not approve:
                state=State.WAITING_APPROVAL; self.memory.add(state.value,"approval_required",f"approval required for {step.tool}",{"step":step.id})
                return {"status":state.value,"plan":[s.__dict__ for s in plan.steps],"trace":trace,"events":self.memory.recent()}
            args=dict(step.arguments);
            if step.tool in {"list_files","read_file","search_text","git_diff"}: args.setdefault("root",self.workspace)
            if step.tool=="run_tests": args.setdefault("cwd",self.workspace)
            try:
                result=TOOLS[step.tool](**args); trace.append({"step":step.id,"tool":step.tool,"result":result}); self.memory.add(state.value,"tool_result",step.tool,{"result":result})
            except Exception as exc:
                state=State.FAILED; self.memory.add(state.value,"error",str(exc),{"tool":step.tool}); return {"status":state.value,"trace":trace,"error":str(exc),"events":self.memory.recent()}
        state=State.COMPLETED; self.memory.add(state.value,"completed","goal completed")
        return {"status":state.value,"trace":trace,"events":self.memory.recent()}
