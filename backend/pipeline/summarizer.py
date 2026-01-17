import numpy as np
from typing import List, Dict
from sklearn.metrics.pairwise import cosine_similarity


def summarize_topic(
    sentences: List[str],
    embeddings: np.ndarray,
    max_sentences: int = 2
) -> str:
    """
    Extractive summary for a single topic.
    """

    if len(sentences) <= max_sentences:
        return " ".join(sentences)

    centroid = embeddings.mean(axis=0, keepdims=True)
    similarities = cosine_similarity(embeddings, centroid).flatten()

    top_indices = similarities.argsort()[-max_sentences:][::-1]
    summary_sentences = [sentences[i] for i in sorted(top_indices)]

    return " ".join(summary_sentences)


def summarize_all_topics(
    topics: Dict[str, List[str]],
    embeddings_map: Dict[str, np.ndarray]
) -> Dict[str, str]:
    """
    Summarize all topics.
    """

    summaries = {}

    for topic, sentences in topics.items():
        summary = summarize_topic(
            sentences,
            embeddings_map[topic]
        )
        summaries[topic] = summary

    return summaries