import os, json
from pathlib import Path
from dotenv import load_dotenv

from services.input_handler import InputHandler
from services.speech_to_text import SpeechToTextService
from services.conversation_separator import ConversationSeparator
from services.groq_summarizer import GroqSummarizer
from services.hf_summarizer import HuggingFaceSummarizer
from services.safe_fallback_summarizer import SafeFallbackSummarizer
from services.summarization_manager import SummarizationManager
from models.transcript import Transcript

# Explicit .env loading (Windows safe)
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

def main():
    file_path = input("Enter audio or text file path: ").strip()

    handler = InputHandler()
    input_data = handler.load(file_path)

    stt = SpeechToTextService()
    separator = ConversationSeparator()

    # 🔀 Route input correctly
    if input_data["type"] == "audio":
        segments = stt.transcribe(input_data["path"])
    else:
        # Convert text into whisper-like segments
        segments = [
            {"text": line}
            for line in input_data["content"].splitlines()
            if line.strip()
        ]

    separated = separator.separate(segments)

    transcript = Transcript(
        separated["agent"],
        separated["customer"]
    )
    transcript_dict = transcript.to_dict()

    groq = GroqSummarizer(os.getenv("GROQ_API_KEY"))
    hf = HuggingFaceSummarizer(os.getenv("HF_API_KEY"))
    safe = SafeFallbackSummarizer()

    manager = SummarizationManager(
        primary=groq,
        fallback=hf,
        emergency=safe
    )

    summary = manager.summarize(transcript_dict)

    output = transcript_dict
    output["summary"] = summary

    os.makedirs("data/outputs", exist_ok=True)
    with open("data/outputs/result.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

    print("✅ Summary generated using:", summary["provider_used"])

if __name__ == "__main__":
    main()
