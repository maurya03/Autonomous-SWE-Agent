from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class State(str, Enum):
    PLANNING="planning"; EXECUTING="executing"; WAITING_APPROVAL="waiting_approval"; COMPLETED="completed"; FAILED="failed"

@dataclass
class Step:
    id: str
    tool: str
    arguments: dict[str, Any] = field(default_factory=dict)
    reason: str = ""
    risk: str = "low"

@dataclass
class Plan:
    goal: str
    steps: list[Step]

@dataclass
class Event:
    state: str
    type: str
    message: str
    data: dict[str, Any] = field(default_factory=dict)
