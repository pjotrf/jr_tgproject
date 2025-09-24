import os, sys, json, urllib.request

token = os.getenv("TELEGRAM_TOKEN")
if not token:
    sys.exit(1)

try:
    with urllib.request.urlopen(f"https://api.telegram.org/bot{token}/getMe", timeout=4) as r:
        data = json.loads(r.read().decode())
    sys.exit(0 if data.get("ok") else 1)
except Exception:
    sys.exit(1)
