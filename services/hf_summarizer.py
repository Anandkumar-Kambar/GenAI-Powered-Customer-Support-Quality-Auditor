import requests
from services.summarizer_base import SummarizerBase


class HuggingFaceSummarizer(SummarizerBase):
    """
    Hugging Face Inference API summarizer with model fallback.
    Best-effort only (free-tier HF behavior).
    """

    MODELS = [
        "facebook/bart-large-cnn",
        "google/pegasus-xsum",
        "sshleifer/distilbart-cnn-12-6"
    ]

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api-inference.huggingface.co/models/"

    def summarize(self, transcript: dict) -> dict:
        text = (
            transcript["speakers"]["customer"][:1200] + " " +
            transcript["speakers"]["agent"][:1200]
        )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": text,
            "options": {
                "wait_for_model": True
            }
        }

        last_error = None

        for model in self.MODELS:
            try:
                response = requests.post(
                    self.base_url + model,
                    headers=headers,
                    json=payload,
                    timeout=60
                )

                if response.status_code != 200:
                    raise Exception(
                        f"{model} failed: {response.status_code}"
                    )

                data = response.json()

                if isinstance(data, list) and "summary_text" in data[0]:
                    summary = data[0]["summary_text"]
                    return {
                        "text": summary,
                        "provider_used": f"huggingface_api ({model})",
                        "word_count": len(summary.split())
                    }

                raise Exception(f"{model} invalid response format")

            except Exception as e:
                last_error = e
                print(f"HF model failed → {model}: {e}")

        # All HF models failed
        raise Exception(f"All HF models failed. Last error: {last_error}")
