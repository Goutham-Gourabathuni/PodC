import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import sent_tokenize
import numpy as np
import logging

logger = logging.getLogger(__name__)

# Ensure NLTK data is available
def ensure_nltk_resources():
    resources = ['punkt', 'punkt_tab']
    for res in resources:
        try:
            nltk.data.find(f'tokenizers/{res}')
        except LookupError:
            logger.info(f"Downloading NLTK resource: {res}")
            nltk.download(res, quiet=True)

ensure_nltk_resources()

def generate_summary(text: str, num_sentences: int = 5) -> str:
    """
    Generates an extractive summary using TF-IDF ranking.
    """
    if not text:
        return ""
        
    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text
        
    try:
        # Basic Top-N sentences using TF-IDF
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(sentences)
        
        # Sum scores for each sentence
        sentence_scores = np.asarray(tfidf_matrix.sum(axis=1)).flatten()
        
        # Get top N indices
        top_indices = sentence_scores.argsort()[-num_sentences:][::-1]
        top_indices.sort() # Keep original order
        
        summary = " ".join([sentences[i] for i in top_indices])
        return summary
    except Exception as e:
        logger.error(f"Summarization failed: {e}")
        # Fallback: return first N sentences
        return " ".join(sentences[:num_sentences])

def extract_topics(text: str, num_topics: int = 5) -> list:
    """
    Extracts key topics/keywords (Placeholder implementation).
    """
    # TODO: Implement better topic extraction (e.g. LDA or noun chunks)
    return ["Placeholder", "Topic", "Extraction"]
