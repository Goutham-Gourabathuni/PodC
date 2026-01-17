from faster_whisper import WhisperModel
from typing import List


class AudioTranscriber:
    def __init__(self, model_size: str = "small"):
        """
        model_size options:
        tiny | base | small | medium | large
        """
        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8"  # CPU optimized
        )

    def transcribe_chunks(self, chunk_paths: List[str]) -> str:
        """
        Transcribe audio chunks and merge into one transcript.
        """
        full_transcript = []

        for chunk_path in chunk_paths:
            print(f"Transcribing: {chunk_path}")
            segments, _ = self.model.transcribe(chunk_path)

            for segment in segments:
                text = segment.text.strip()
                if text:
                    full_transcript.append(text)

        return " ".join(full_transcript)