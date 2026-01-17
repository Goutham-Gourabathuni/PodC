from backend.pipeline.audio_loader import normalize_audio

input_audio = "backend/storage/audio/62dbc57a-6dfa-447c-82c8-f2eddce93409.wav"
output_audio = normalize_audio(input_audio)

print("Normalized audio saved at:", output_audio)