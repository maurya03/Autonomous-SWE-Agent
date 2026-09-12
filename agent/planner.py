import json
from .models import Plan,Step
from .tools import TOOLS

def deterministic_plan(goal):
    g=goal.lower(); steps=[Step("inspect","list_files",{},"inspect the workspace")];
    if any(x in g for x in ("search","find","locate")): steps.append(Step("search","search_text",{"query":goal},"locate relevant code"))
    if "test" in g or "bug" in g: steps.append(Step("tests","run_tests",{},"establish the current test state","medium"))
    if "diff" in g or "changes" in g: steps.append(Step("diff","git_diff",{},"inspect working-tree changes"))
    return Plan(goal,steps)

def parse_plan(goal,text):
    obj=json.loads(text); steps=[]
    for i,raw in enumerate(obj.get("steps",[]),1):
        name=raw["tool"]
        if name not in TOOLS: raise ValueError(f"planner selected disallowed tool: {name}")
        steps.append(Step(raw.get("id",f"step-{i}"),name,raw.get("arguments",{}),raw.get("reason",""),raw.get("risk","low")))
    return Plan(goal,steps)
