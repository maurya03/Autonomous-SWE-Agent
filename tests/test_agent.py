import json
from agent.runner import Agent
from agent.mcp_server import handle
from agent.evaluator import evaluate

def test_mcp_initialize_and_list():
 r=handle({"jsonrpc":"2.0","id":1,"method":"initialize"}); assert r["result"]["serverInfo"]["name"]=="ase-tools"
 r=handle({"jsonrpc":"2.0","id":2,"method":"tools/list"}); assert {"name":"run_tests","description":"run_tests tool"} in r["result"]["tools"]

def test_approval_gate(tmp_path):
 r=Agent(str(tmp_path),str(tmp_path/"m.db")).run("run tests")
 assert r["status"]=="waiting_approval" and r["plan"][1]["tool"]=="run_tests"

def test_execution_and_memory(tmp_path):
 (tmp_path/"hello.txt").write_text("authentication token")
 r=Agent(str(tmp_path),str(tmp_path/"m.db")).run("find authentication code")
 assert r["status"]=="completed" and [x["tool"] for x in r["trace"]]==["list_files","search_text"]
 assert any(x["type"]=="tool_result" for x in r["events"])

def test_evaluation():
 r={"status":"completed","trace":[{"tool":"list_files"},{"tool":"search_text"}]}
 m=evaluate(r,["list_files","search_text"]); assert m["success"] and m["precision"]==1.0
