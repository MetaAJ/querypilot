"""Event contract for rendering TrueForge-backed agent activity."""

from enum import StrEnum

from pydantic import BaseModel, Field


class EventType(StrEnum):
    THOUGHT = "thought"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    SANDBOX = "sandbox"
    APPROVAL_REQUIRED = "approval_required"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentEvent(BaseModel):
    type: EventType
    title: str
    detail: str
    sequence: int = Field(ge=0)
    metadata: dict[str, str] = Field(default_factory=dict)


def local_demo_events() -> list[AgentEvent]:
    """Return the activity sequence used before live TrueForge streaming is connected."""
    return [
        AgentEvent(type=EventType.THOUGHT, title="Question understood", detail="Metric contract created", sequence=0),
        AgentEvent(type=EventType.TOOL_CALL, title="Schema inspected", detail="inspect_schema via MCP", sequence=1),
        AgentEvent(type=EventType.TOOL_CALL, title="Query executed", detail="Read-only SQL via MCP", sequence=2),
        AgentEvent(type=EventType.SANDBOX, title="Forecast computed", detail="Python executed in Daytona", sequence=3),
        AgentEvent(type=EventType.APPROVAL_REQUIRED, title="Human checkpoint", detail="Approval required before export", sequence=4),
    ]
