import re
import nltk
import spacy
from typing import List

nlp = spacy.load("en_core_web_sm")


def preprocess_text(text: str) -> List[str]:
    """
    Clean transcript text and split into sentences.
    """

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Lowercase (optional)
    text = text.lower()

    # Sentence segmentation (spaCy)
    doc = nlp(text)
    sentences = []

    for sent in doc.sents:
        sent_text = sent.text.strip()

        # Remove very short/noisy sentences
        if len(sent_text.split()) >= 3:
            sentences.append(sent_text)

    return sentences