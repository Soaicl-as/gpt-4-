from datetime import datetime

def log(msg: str):
    print(f"[{datetime.utcnow().isoformat()}] {msg}")
