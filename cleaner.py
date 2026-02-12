import re

class TranscriptCleaner:
    def clean(self, text: str) -> str:
        text = text.lower()
        text = text.replace("\n", " ")
        text = re.sub(r"[^a-z0-9\s.,!?']", "", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()