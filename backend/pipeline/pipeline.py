import os
from typing import Dict, List

from backend.pipeline.audio_loader import normalize_audio
from backend.pipeline.audio_chunker import chunk_audio
from backend.pipeline.transcriber import AudioTranscriber
from backend.pipeline.text_preprocessor import preprocess_text
from backend.pipeline.embedding_generator import EmbeddingGenerator
from backend.pipeline.topic_segmenter import segment_topics
from backend.pipeline.topic_labeler import label_topic
from backend.pipeline.summarizer import summarize_topic
from backend.pipeline.pdf_generator import generate_pdf
from backend.pipeline.docx_generator import generate_docx


def run_full_pipeline(
    audio_path: str,
    output_dir: str = "backend/storage/output"
) -> Dict:
    """
    Run the full podcast summarization pipeline.
    """

    os.makedirs(output_dir, exist_ok=True)

    # 1. Normalize audio
    normalized_audio = normalize_audio(audio_path)

    # 2. Chunk audio
    chunks = chunk_audio(normalized_audio)

    # 3. Transcribe
    transcriber = AudioTranscriber()
    transcript = transcriber.transcribe_chunks(chunks)

    # 4. Text preprocessing
    sentences = preprocess_text(transcript)

    # 5. Embeddings
    embedder = EmbeddingGenerator()
    embeddings = embedder.generate(sentences)

    # 6. Topic segmentation
    topic_sentence_groups = segment_topics(sentences, embeddings)

    # 7. Topic labeling + summarization
    topic_summaries = {}
    embeddings_map = {}

    idx = 0
    for group in topic_sentence_groups:
        group_len = len(group)
        group_embeddings = embeddings[idx: idx + group_len]
        idx += group_len

        topic_label = label_topic(group)
        summary = summarize_topic(group, group_embeddings)

        topic_summaries[topic_label] = summary
        embeddings_map[topic_label] = group_embeddings

    # 8. Generate outputs
    pdf_path = os.path.join(output_dir, "podcast_summary.pdf")
    docx_path = os.path.join(output_dir, "podcast_summary.docx")

    generate_pdf(topic_summaries, pdf_path)
    generate_docx(topic_summaries, docx_path)

    return {
        "transcript": transcript,
        "topics": topic_summaries,
        "pdf_path": pdf_path,
        "docx_path": docx_path
    }