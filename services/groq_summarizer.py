import requests
from services.summarizer_base import SummarizerBase

class GroqSummarizer(SummarizerBase):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def summarize(self, transcript: dict) -> dict:
        # aggressive truncation
        customer = transcript["speakers"]["customer"][:1200]
        agent = transcript["speakers"]["agent"][:1200]

        prompt = (
            "You are a customer support quality auditor.\n"
            "Summarize the interaction below in under 150 words.\n"
            "Focus on:\n"
            "- Customer issue\n"
            "- Agent response quality\n"
            "- Resolution status\n\n"
            f"Customer:\n{customer}\n\n"
            f"Agent:\n{agent}"
        )

        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are an expert customer support quality auditor."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "top_p": 0.9,
            "max_tokens": 250,
            "stream": False
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            self.url,
            json=payload,
            headers=headers,
            timeout=30
        )

        # DEBUG helper (keep for now)
        if response.status_code != 200:
            raise Exception(f"Groq error {response.status_code}: {response.text}")

        data = response.json()
        text = data["choices"][0]["message"]["content"]

        return {
            "text": text,
            "provider_used": "groq",
            "word_count": len(text.split())
        }
