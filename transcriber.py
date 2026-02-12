import whisper

class Transcriber:
    def __init__(self):
        self.model = whisper.load_model("base")

    def transcribe_audio(self, file_path: str) -> str:
        result = self.model.transcribe(
            file_path,
            language="en",
            task="transcribe"
        )
        return result["text"]

    def transcribe_text(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()