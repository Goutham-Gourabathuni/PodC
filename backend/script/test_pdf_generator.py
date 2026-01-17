from backend.pipeline.pdf_generator import generate_pdf

print(">>> test_pdf_generator STARTED <<<")

summaries = {
    "Learning Machine Subset": "Machine learning and deep learning are core AI techniques.",
    "Health Fitness": "Exercise and nutrition are essential for good health."
}

output_pdf = "backend/storage/output/podcast_summary.pdf"

generate_pdf(summaries, output_pdf, title="Test Podcast Summary")

print("PDF generated at:", output_pdf)

print(">>> test_pdf_generator FINISHED <<<")