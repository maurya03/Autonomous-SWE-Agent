# Autonomous-SWE-Agent

An inspectable software-engineering agent architecture that plans bounded tool calls, persists its trajectory, enforces approval gates, exposes tools through an MCP-style JSON-RPC boundary, and evaluates tool-selection behavior. It is deliberately designed so autonomy never bypasses runtime policy.

## Architecture

```text
User Goal
   │
   ▼
 Planner ───────────────► optional OpenAI-compatible LLM
   │
   ▼
 State Machine
 planning → executing → completed
                  │
                  ├── failed
                  └── waiting_approval
   │
   ▼
 Tool Policy / Allow-list
   │
   ├── list_files       ├── search_text
   ├── read_file        ├── git_diff
   ├── calculate        └── run_tests (approval)
   │
   ├──────────────► SQLite trajectory memory
   │
   └──────────────► MCP JSON-RPC tool server

Evaluation → precision / recall / exact tool sequence
```

## Engineering properties

- deterministic planner for key-free, reproducible demos
- optional OpenAI-compatible planning adapter
- explicit tool allow-list
- workspace traversal protection
- bounded test subprocesses and output capture
- human approval gate for medium-risk execution
- SQLite trajectory/event memory
- explicit execution state machine
- structured tool results and failure states
- MCP-style `initialize`, `tools/list`, and `tools/call` JSON-RPC boundary
- evaluation of expected tool sequences
- CI with pytest

## Run

```bash
pip install -e ".[test]"
pytest -q
python -m agent.cli "inspect repository"
python -m agent.cli "find authentication code" --workspace .
python -m agent.cli "inspect repository and run tests" --approve
```

The deterministic planner is intentionally simple: it is a reliable runtime baseline, not a claim of human-level autonomy.

## MCP boundary

Run the dependency-free server:

```bash
python -m agent.mcp_server
```

It accepts one JSON-RPC request per line and exposes the same policy-controlled tool registry.

## Optional model planning

```bash
export LLM_API_KEY=...
export LLM_MODEL=...
python -m agent.cli "inspect the repository and run tests" --llm --approve
```

The model only proposes a plan. The runtime validates tool names, applies workspace and approval policies, and executes the selected tools.

## Evaluation

`evals/agent_cases.json` defines deterministic expectations for representative tasks. The evaluator reports tool-sequence precision, recall, and success.

## Deliberate scope

This is a local agent runtime, not a production coding agent. It does not claim unrestricted code modification, cloud execution, autonomous GitHub operations, or sandbox isolation. Those require stronger permissioning and infrastructure.

## Portfolio connection

```text
MiniDB → storage
TinyC → compiler
PrivateSearchEngine → indexing/ranking
EngineeringRAG → retrieval/evaluation
Autonomous-SWE-Agent → agents/tools/memory/MCP
AI-Native-AWS-Platform → cloud/deployment/observability
```
