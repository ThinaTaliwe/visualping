from datetime import datetime
from pydantic import BaseModel, Field


class VisualpingEvent(BaseModel):
    check_id: str
    url: str
    title: str | None = None
    trigger_time: datetime = Field(default_factory=datetime.utcnow)
    old_text: str | None = None
    new_text: str


class TradeDecision(BaseModel):
    pair: str
    side: str
    confidence: float
    reason: str


class OrderRequest(BaseModel):
    pair: str
    side: str
    units: int


class WebhookAck(BaseModel):
    status: str
    message: str
