from fastapi import Depends, FastAPI, Header, HTTPException
from sqlmodel import Session
from app.config import settings
from app.database import get_session, init_db
from app.order_service import process_event
from app.schemas import VisualpingEvent, WebhookAck


app = FastAPI(title="Visualping FX Bot", version="0.1.0")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/webhooks/visualping", response_model=WebhookAck)
def receive_visualping(
    payload: VisualpingEvent,
    session: Session = Depends(get_session),
    x_webhook_token: str | None = Header(default=None),
) -> WebhookAck:
    if x_webhook_token != settings.visualping_webhook_token:
        raise HTTPException(status_code=401, detail="Invalid webhook token")

    result = process_event(session, payload)
    return WebhookAck(status="accepted", message=f"Action: {result.action}; Reason: {result.reason}")
