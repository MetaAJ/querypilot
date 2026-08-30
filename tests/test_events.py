from querypilot.events import EventType, local_demo_events


def test_demo_events_are_ordered_and_include_safety_checkpoint() -> None:
    events = local_demo_events()
    assert [event.sequence for event in events] == list(range(len(events)))
    assert events[1].type is EventType.TOOL_CALL
    assert events[-1].type is EventType.APPROVAL_REQUIRED
