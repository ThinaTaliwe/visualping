from datetime import datetime
from sqlmodel import SQLModel, Field


class DecisionLog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    check_id: str
    event_hash: str = Field(index=True, unique=True)
    pair: str | None = None
    side: str | None = None
    confidence: float | None = None
    action: str
    reason: str


class Position(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    pair: str
    side: str
    units: int
    entry_price: float | None = None


class DailyPnl(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    day: str = Field(index=True, unique=True)
    pnl_pct: float
