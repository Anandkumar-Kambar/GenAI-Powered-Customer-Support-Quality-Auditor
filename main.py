import json
import os
from transcriber import Transcriber
from cleaner import TranscriptCleaner
from schema import Transcript

def main():
    file_path = input("Enter English audio or text file path: ").strip()
    extension = file_path.split(".")[-1].lower()

    transcriber = Transcriber()
    cleaner = TranscriptCleaner()

    if extension in ["wav", "mp3", "m4a"]:
        raw_text = transcriber.transcribe_audio(file_path)
        source = "audio"
    elif extension == "txt":
        raw_text = transcriber.transcribe_text(file_path)
        source = "text"
    else:
        print("Unsupported file type")
        return

    cleaned_text = cleaner.clean(raw_text)

    transcript = Transcript(
        source=source,
        raw_text=raw_text,
        cleaned_text=cleaned_text
    )

    os.makedirs("output", exist_ok=True)
    with open("output/transcript.json", "w", encoding="utf-8") as f:
        json.dump(transcript.to_dict(), f, indent=4)

    print("\nTranscript generated successfully (English only):\n")
    print(cleaned_text)

if __name__ == "__main__":
    main()