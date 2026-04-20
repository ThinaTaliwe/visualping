from app.schemas import VisualpingEvent
from app.strategy import classify_event


def test_classify_hawkish_signal() -> None:
    event = VisualpingEvent(
        check_id="1",
        url="https://example.com",
        new_text="The latest release sounds hawkish",
    )
    decision = classify_event(event)
    assert decision is not None
    assert decision.pair == "EUR_USD"
    assert decision.side == "SELL"


def test_classify_no_signal() -> None:
    event = VisualpingEvent(
        check_id="2",
        url="https://example.com",
        new_text="No market-moving changes",
    )
    assert classify_event(event) is None
