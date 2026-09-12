import argparse,json
from .runner import Agent
from .llm import OpenAICompatibleClient
def main():
    p=argparse.ArgumentParser(description="Inspectable autonomous software engineer")
    p.add_argument("goal"); p.add_argument("--workspace",default="."); p.add_argument("--memory",default="agent.db"); p.add_argument("--approve",action="store_true"); p.add_argument("--llm",action="store_true")
    a=p.parse_args(); llm=OpenAICompatibleClient() if a.llm else None
    print(json.dumps(Agent(a.workspace,a.memory,llm).run(a.goal,a.approve),indent=2,default=str))

if __name__=="__main__": main()
