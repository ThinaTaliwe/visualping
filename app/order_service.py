from sqlmodel import Session, select
from app.broker.paper import PaperBroker
from app.idempotency import event_hash
from app.models import DecisionLog, Position
from app.risk import RiskError, evaluate_risk
from app.schemas import VisualpingEvent
from app.strategy import classify_event


broker = PaperBroker()


def process_event(session: Session, event: VisualpingEvent) -> DecisionLog:
    digest = event_hash(event)

    existing = session.exec(select(DecisionLog).where(DecisionLog.event_hash == digest)).first()
    if existing:
        return existing

    decision = classify_event(event)
    if decision is None:
        log = DecisionLog(
            check_id=event.check_id,
            event_hash=digest,
            action="ignored",
            reason="No strategy keyword matched",
        )
        session.add(log)
        session.commit()
        session.refresh(log)
        return log

    try:
        order = evaluate_risk(session, decision)
    except RiskError as exc:
        log = DecisionLog(
            check_id=event.check_id,
            event_hash=digest,
            pair=decision.pair,
            side=decision.side,
            confidence=decision.confidence,
            action="blocked",
            reason=str(exc),
        )
        session.add(log)
        session.commit()
        session.refresh(log)
        return log

    order_id = broker.place_market_order(order)
    session.add(
        Position(
            pair=order.pair,
            side=order.side,
            units=order.units,
        )
    )
    log = DecisionLog(
        check_id=event.check_id,
        event_hash=digest,
        pair=decision.pair,
        side=decision.side,
        confidence=decision.confidence,
        action="executed",
        reason=f"Order placed: {order_id}",
    )
    session.add(log)
    session.commit()
    session.refresh(log)
    return log
