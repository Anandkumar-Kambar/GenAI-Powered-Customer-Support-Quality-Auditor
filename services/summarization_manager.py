class SummarizationManager:
    def __init__(self, primary, fallback, emergency):
        self.primary = primary
        self.fallback = fallback
        self.emergency = emergency

    def summarize(self, transcript: dict) -> dict:
        try:
            return self.primary.summarize(transcript)
        except Exception as e:
            print("Primary summarizer failed:", e)
            try:
                return self.fallback.summarize(transcript)
            except Exception as e:
                print("Fallback summarizer failed:", e)
                return self.emergency.summarize(transcript)
