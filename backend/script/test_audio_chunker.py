import sys
import os

# Add backend to sys.path to allow importing pipeline
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.pipeline.audio_chunker import chunk_audio

audio_file = "backend/storage/audio/62dbc57a-6dfa-447c-82c8-f2eddce93409_normalized.wav"
chunks = chunk_audio(audio_file, chunk_duration=30)

print("Created chunks:")
for c in chunks:
    print(c)
