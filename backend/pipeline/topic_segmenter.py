import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List


def segment_topics(
    sentences: List[str],
    embeddings: np.ndarray,
    similarity_threshold: float = 0.65
) -> List[List[str]]:
    """
    Segment sentences into topics based on cosine similarity.
    """

    if len(sentences) == 0:
        return []

    topics = []
    current_topic = [sentences[0]]

    for i in range(1, len(sentences)):
        sim = cosine_similarity(
            embeddings[i - 1].reshape(1, -1),
            embeddings[i].reshape(1, -1)
        )[0][0]

        if sim < similarity_threshold:
            topics.append(current_topic)
            current_topic = [sentences[i]]
        else:
            current_topic.append(sentences[i])

    topics.append(current_topic)
    return topics