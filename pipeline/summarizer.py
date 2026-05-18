# pipeline/summarizer.py

"""
Abstractive Topic Summarization Module
Uses HuggingFace BART to generate concise, meaningful summaries
"""

import logging
import os
import re

logger = logging.getLogger(__name__)

_summarizer = None
SUMMARIZER_MODEL = os.getenv("SUMMARIZER_MODEL", "facebook/bart-large-cnn")
MIN_WORDS_FOR_MODEL = int(os.getenv("MIN_WORDS_FOR_SUMMARY_MODEL", "55"))


def _get_summarizer():
    """
    Lazy-load the summarization model
    """
    global _summarizer
    if _summarizer is None:
        try:
            from transformers import pipeline

            logger.info("Loading summarization model: %s", SUMMARIZER_MODEL)
            _summarizer = pipeline(
                "summarization",
                model=SUMMARIZER_MODEL,
                device=-1  # CPU (safe)
            )
            logger.info("Summarization model loaded")
        except Exception as e:
            logger.warning(f"⚠️ Failed to load summarizer: {e}")
            _summarizer = False

    return _summarizer if _summarizer else None


def _chunk_text(text, max_words=180):
    """
    Split long text into chunks for BART
    """
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i:i + max_words])


def _extractive_summary(text, max_sentences=2, max_chars=450):
    """
    Cheap fallback for short topic segments where BART would be slower
    and less reliable than preserving the original wording.
    """
    cleaned = " ".join(text.split())
    if not cleaned:
        return ""

    sentences = [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", cleaned)
        if sentence.strip()
    ]
    summary = " ".join(sentences[:max_sentences]) if sentences else cleaned
    return summary[:max_chars].rstrip()


def _lengths_for_chunk(word_count, max_length, min_length):
    """
    Keep generation lengths below the input size to avoid Transformers
    warnings and wasted decoding on short chunks.
    """
    chunk_max = min(max_length, max(12, int(word_count * 0.65)))
    chunk_min = min(min_length, max(5, chunk_max // 2))

    if chunk_min >= chunk_max:
        chunk_min = max(1, chunk_max - 2)

    return chunk_max, chunk_min


def summarize_text(text, max_length=40, min_length=25):
    """
    Generate an abstractive summary of the given text.
    """

    cleaned = " ".join(text.split())
    word_count = len(cleaned.split())

    if not cleaned:
        return ""

    if word_count < MIN_WORDS_FOR_MODEL:
        return _extractive_summary(cleaned)

    summarizer = _get_summarizer()

    # Fallback if model unavailable
    if not summarizer:
        return _extractive_summary(cleaned)

    summaries = []

    try:
        for chunk in _chunk_text(cleaned):
            chunk_word_count = len(chunk.split())
            if chunk_word_count < MIN_WORDS_FOR_MODEL:
                summaries.append(_extractive_summary(chunk))
                continue

            chunk_max, chunk_min = _lengths_for_chunk(
                word_count=chunk_word_count,
                max_length=max_length,
                min_length=min_length
            )

            summary = summarizer(
                chunk,
                max_length=chunk_max,
                min_length=chunk_min,
                do_sample=False
            )
            if summary and isinstance(summary, list):
                summaries.append(summary[0]["summary_text"])

        # Final compression if multiple chunks
        final_summary = " ".join(summaries)

        if len(final_summary.split()) > max_length * 2:
            final_max, final_min = _lengths_for_chunk(
                word_count=len(final_summary.split()),
                max_length=max_length,
                min_length=min_length
            )
            final_summary = summarizer(
                final_summary,
                max_length=final_max,
                min_length=final_min,
                do_sample=False
            )[0]["summary_text"]

        return final_summary.strip()

    except Exception as e:
        logger.warning("Summarization failed: %s", e)
        return _extractive_summary(cleaned)
