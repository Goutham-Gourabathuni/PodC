from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from typing import Dict
import os


def generate_pdf(
    summaries: Dict[str, str],
    output_path: str,
    title: str = "Podcast Summary"
):
    """
    Generate a PDF with topic-wise summaries.
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph(f"<b>{title}</b>", styles["Title"]))
    story.append(Spacer(1, 20))

    # Topics
    for topic, summary in summaries.items():
        story.append(Paragraph(f"<b>{topic}</b>", styles["Heading2"]))
        story.append(Spacer(1, 10))
        story.append(Paragraph(summary, styles["BodyText"]))
        story.append(Spacer(1, 20))

    doc.build(story)