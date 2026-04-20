# Visualping FX Bot (Scaffold)

This repository now contains a production-oriented scaffold for an automated FX trading system driven by Visualping updates.

## What is implemented

- FastAPI service with:
  - `GET /health`
  - `POST /webhooks/visualping` protected by `X-Webhook-Token`
- Event idempotency hash so duplicate updates are not re-executed.
- Rule-based strategy classifier from Visualping text to FX decisions.
- Risk engine with confidence threshold, daily loss guard, and open-position cap.
- Paper broker adapter for safe non-live execution.
- SQLModel persistence for decision logs and positions.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

Set env vars as needed:

```bash
export FXBOT_VISUALPING_WEBHOOK_TOKEN='change-me'
export FXBOT_DATABASE_URL='sqlite:///./fxbot.db'
```

## Example webhook payload

```json
{
  "check_id": "abc123",
  "url": "https://example.com/calendar",
  "title": "Macro calendar changed",
  "new_text": "Fed statement turned hawkish",
  "old_text": "Fed statement unchanged"
}
```

Use header:

```text
X-Webhook-Token: change-me
```

## Next steps

- Add real broker adapter (OANDA/IBKR) with signed auth and retries.
- Add asynchronous queue processing (Celery/RQ).
- Add order reconciliation job and PnL marking.
- Add structured logging/metrics and alerting.
- Add robust backtesting and forward-testing pipeline.
