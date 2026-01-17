from backend.pipeline.transcriber import AudioTranscriber

chunk_files = [
    "backend/storage/audio/62dbc57a-6dfa-447c-82c8-f2eddce93409_normalized_chunk_000.wav",
    "backend/storage/audio/62dbc57a-6dfa-447c-82c8-f2eddce93409_normalized_chunk_001.wav",
]

transcriber = AudioTranscriber(model_size="small")
transcript = transcriber.transcribe_chunks(chunk_files)

print("\n--- TRANSCRIPT ---\n")
print(transcript)