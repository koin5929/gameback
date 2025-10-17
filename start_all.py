import os, sys, threading, asyncio, uvicorn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ensure Python can find our packages
sys.path.append(os.path.join(BASE_DIR, "backend"))  # so 'from backend.main import app' works (inner package)
sys.path.append(os.path.join(BASE_DIR, "bot"))      # so 'from bot.bot_module import run_bot' works

from backend.main import app
from bot.bot_module import run_bot

def run_api():
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

def run_discord():
    # RUN_DISCORD_BOT=true 일 때만 구동
    if os.getenv("RUN_DISCORD_BOT", "true").lower() == "true":
        asyncio.run(run_bot())

if __name__ == "__main__":
    t = threading.Thread(target=run_api, daemon=True)
    t.start()
    run_discord()
