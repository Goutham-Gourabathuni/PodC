from typing import List
from collections import Counter
import re


def label_topic(sentences: List[str], top_k: int = 3) -> str:
    """
    Generate a short topic label from a list of sentences.
    """

    text = " ".join(sentences)

    # Basic cleanup
    words = re.findall(r"[a-zA-Z]{3,}", text.lower())

    stopwords = {
        "the", "and", "for", "with", "that", "this",
        "from", "about", "into", "your", "have", "are",
        "was", "were", "will", "their", "they"
    }

    keywords = [w for w in words if w not in stopwords]

    if not keywords:
        return "General"

    most_common = Counter(keywords).most_common(top_k)
    label = " ".join(word for word, _ in most_common)

    return label.title()