from pathlib import Path
import json
from datetime import datetime

class Logs:
    def __init__(self, path: str = "logs/"):
        logs_dir = Path(path)
        logs_dir.mkdir(parents=True, exist_ok=True)  # Make sure the folder exists
        self.path = logs_dir / "logs.jsonl"
        
        self.path.touch()
        self.file = self.path.open("a") # Open the file in append mode ("a")

    def log(self, message: dict):
        self.file.write(json.dumps(message) + "\n")
        
    def log_reconnect(self, ip: str):
        return self.log({
            "timestamp": datetime.now().isoformat(),
            "status": "reconnected",
            "ip": ip
        })
        
    def log_disconnect(self, ip: str):
        return self.log({
            "timestamp": datetime.now().isoformat(),
            "status": "disconnected",
            "ip": ip
        })  