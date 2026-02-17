class SafeFallbackSummarizer:
    def summarize(self, transcript: dict) -> dict:
        customer = transcript["speakers"]["customer"][:300]
        agent = transcript["speakers"]["agent"][:300]

        text = (
            "The customer contacted support regarding an issue. "
            "The agent responded and attempted to assist. "
            "Further analysis may be required to fully assess resolution quality."
        )

        return {
            "text": text,
            "provider_used": "safe_fallback",
            "word_count": len(text.split())
        }
