import uuid
from datetime import datetime

class Transcript:
    def __init__(self, source: str, raw_text: str, cleaned_text: str):
        self.data = {
            "id": str(uuid.uuid4()),
            "language": "en",
            "source": source,
            "created_at": datetime.utcnow().isoformat(),
            "raw_text": raw_text,
            "cleaned_text": cleaned_text
        }

    def to_dict(self):
        return self.data