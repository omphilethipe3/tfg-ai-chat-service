# tfg-ai-chat-service

A containerized Python chat service integrating TFG’s Domain API with an AI agent backend.

## Quickstart

```bash
# 1. Create & activate venv
python3 -m venv .venv
source .venv/bin/activate

# 2. Install deps
pip install fastapi uvicorn

# 3. Run health check
uvicorn src.api.main:app --reload
curl http://127.0.0.1:8000/health