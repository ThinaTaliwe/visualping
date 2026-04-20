from datetime import datetime

from sqlmodel import Session, SQLModel, create_engine

from app.models import DailyPnl, Position
from app.risk import RiskError, evaluate_risk
from app.schemas import TradeDecision


def make_session() -> Session:
    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)
    return Session(engine)


def test_risk_blocks_low_confidence() -> None:
    with make_session() as session:
        decision = TradeDecision(pair="EUR_USD", side="BUY", confidence=0.4, reason="x")
        try:
            evaluate_risk(session, decision)
            assert False, "Expected RiskError"
        except RiskError:
            assert True


def test_risk_blocks_daily_loss_limit() -> None:
    with make_session() as session:
        session.add(DailyPnl(day=datetime.utcnow().date().isoformat(), pnl_pct=-0.1))
        session.commit()

        decision = TradeDecision(pair="EUR_USD", side="BUY", confidence=0.8, reason="x")
        try:
            evaluate_risk(session, decision)
            assert False, "Expected RiskError"
        except RiskError as exc:
            assert "Daily loss limit" in str(exc)


def test_risk_blocks_max_open_positions() -> None:
    with make_session() as session:
        for _ in range(3):
            session.add(Position(pair="EUR_USD", side="BUY", units=1))
        session.commit()

        decision = TradeDecision(pair="EUR_USD", side="BUY", confidence=0.8, reason="x")
        try:
            evaluate_risk(session, decision)
            assert False, "Expected RiskError"
        except RiskError as exc:
            assert "Max open positions" in str(exc)
