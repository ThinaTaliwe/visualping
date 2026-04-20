from datetime import datetime
from sqlmodel import Session, select
from app.config import settings
from app.models import DailyPnl, Position
from app.schemas import OrderRequest, TradeDecision


class RiskError(Exception):
    pass


def _today() -> str:
    return datetime.utcnow().date().isoformat()


def evaluate_risk(session: Session, decision: TradeDecision, equity: float = 10_000) -> OrderRequest:
    if decision.confidence < 0.60:
        raise RiskError("Confidence too low")

    open_positions = session.exec(select(Position)).all()
    if len(open_positions) >= settings.max_open_positions:
        raise RiskError("Max open positions reached")

    pnl_row = session.exec(select(DailyPnl).where(DailyPnl.day == _today())).first()
    if pnl_row and pnl_row.pnl_pct <= -settings.max_daily_loss_pct:
        raise RiskError("Daily loss limit reached")

    risk_dollars = equity * settings.max_risk_per_trade_pct
    units = max(int(risk_dollars), 1)
    units = min(units, settings.default_order_units)
    return OrderRequest(pair=decision.pair, side=decision.side, units=units)
