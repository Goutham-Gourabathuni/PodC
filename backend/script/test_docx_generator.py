from backend.pipeline.docx_generator import generate_docx

print(">>> test_docx_generator STARTED <<<")

summaries = {
    "Learning Machine Subset": "Machine learning and deep learning are core AI techniques.",
    "Health Fitness": "Exercise and nutrition are essential for good health."
}

output_docx = "backend/storage/output/podcast_summary.docx"

generate_docx(summaries, output_docx, title="Test Podcast Summary")

print("DOCX generated at:", output_docx)

print(">>> test_docx_generator FINISHED <<<")