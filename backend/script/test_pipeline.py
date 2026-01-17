from backend.pipeline.pipeline import run_full_pipeline

audio_file = "backend/storage/audio/fc54e8f6-3f42-4288-b3b0-3f0f1795a76a.wav"

result = run_full_pipeline(audio_file)

print("\n--- TOPIC SUMMARIES ---")
for topic, summary in result["topics"].items():
    print(f"\n{topic}:")
    print(summary)

print("\nPDF:", result["pdf_path"])
print("DOCX:", result["docx_path"])
