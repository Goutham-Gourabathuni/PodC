from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

def generate_pdf_report(title: str, summary: str, topics: list, output_path: str) -> str:
    """
    Generates a PDF report using ReportLab.
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(output_path)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    story.append(Paragraph(f"Summary Report: {title}", styles['Title']))
    story.append(Spacer(1, 12))
    
    # Topics
    if topics:
        topic_text = ", ".join(topics)
        story.append(Paragraph(f"<b>Key Topics:</b> {topic_text}", styles['Normal']))
        story.append(Spacer(1, 12))
    
    # Summary
    story.append(Paragraph("Executive Summary", styles['Heading2']))
    if summary:
        story.append(Paragraph(summary, styles['BodyText']))
    else:
        story.append(Paragraph("No summary available.", styles['BodyText']))
    
    doc.build(story)
    return output_path
