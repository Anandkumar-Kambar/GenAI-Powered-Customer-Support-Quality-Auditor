import uuid
from datetime import datetime

class Transcript:
    def __init__(self, agent_text: str, customer_text: str):
        self.data = {"conversation_id": str(uuid.uuid4()), "language": "en", "created_at": datetime.utcnow().isoformat(), "speakers": {"agent": agent_text, "customer": customer_text}}

    def to_dict(self):
        return self.data
