# Visualping FX Bot (Scaffold)

This repository contains a production-oriented scaffold for an automated FX trading system driven by Visualping updates.

## VS Code + Server setup (fixes the exact errors you hit)

### 1) Clone and enter the **actual repo folder**
Your `git status` error happened because you ran Git commands from `/opt/Bot_Visualping` instead of `/opt/Bot_Visualping/visualping`.

```bash
cd /opt/Bot_Visualping
git clone https://github.com/ThinaTaliwe/visualping.git
cd visualping
```

Now this should work:

```bash
git status
```

### 2) If you accidentally ran `git init` in the parent folder
You created an extra Git repo in `/opt/Bot_Visualping/.git`. Remove it:

```bash
cd /opt/Bot_Visualping
rm -rf .git
cd visualping
git status
```

### 3) Use Python 3 (not `python`)
On Debian/Ubuntu servers, `python` may not exist by default. Use `python3`.

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
```

### 4) Create virtual env + install dependencies
Use one command:

```bash
./scripts/bootstrap.sh
```

Or manually:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .[dev]
```

### 5) Run the API

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

### 6) Open in VS Code
- Use **Remote - SSH** to open `/opt/Bot_Visualping/visualping`.
- Recommended extensions are in `.vscode/extensions.json`.
- Interpreter auto-points to `.venv/bin/python` via `.vscode/settings.json`.
- You can run/debug `uvicorn` using `.vscode/launch.json`.

## Makefile shortcuts

```bash
make install   # create venv + install deps
make run       # run uvicorn
make test      # run pytest
make compile   # python -m compileall app tests
```

## What is implemented

- FastAPI service with:
  - `GET /health`
  - `POST /webhooks/visualping` protected by `X-Webhook-Token`
- Event idempotency hash so duplicate updates are not re-executed.
- Rule-based strategy classifier from Visualping text to FX decisions.
- Risk engine with confidence threshold, daily loss guard, and open-position cap.
- Paper broker adapter for safe non-live execution.
- SQLModel persistence for decision logs and positions.

## Environment variables

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
