import whisper

class SpeechToTextService:
    def __init__(self, model_size="base"):
        self.model = whisper.load_model(model_size)

    def transcribe(self, audio_path: str):
        result = self.model.transcribe(audio_path, language="en", task="transcribe")
        return result["segments"]
