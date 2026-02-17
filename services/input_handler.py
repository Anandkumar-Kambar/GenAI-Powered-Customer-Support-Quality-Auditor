from pathlib import Path

class InputHandler:
    AUDIO_EXTENSIONS = {".wav", ".mp3", ".m4a"}

    def load(self, file_path: str) -> dict:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError("Input file not found")

        ext = path.suffix.lower()

        if ext in self.AUDIO_EXTENSIONS:
            return {
                "type": "audio",
                "path": str(path)
            }

        if ext == ".txt":
            with open(path, "r", encoding="utf-8") as f:
                return {
                    "type": "text",
                    "content": f.read()
                }

        raise ValueError(
            "Unsupported file type. Only audio (.wav, .mp3, .m4a) "
            "and text (.txt) files are allowed."
        )
