from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np


class EmbeddingGenerator:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Lightweight, fast, and very good semantic model.
        """
        self.model = SentenceTransformer(model_name)

    def generate(self, sentences: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of sentences.
        """
        embeddings = self.model.encode(
            sentences,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        return embeddings