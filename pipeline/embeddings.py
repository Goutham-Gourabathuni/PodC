import os

from sentence_transformers import SentenceTransformer

_model = None
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

def get_embedding_model():
    global _model
    if _model is None:
        print(f"Loading embedding model: {EMBEDDING_MODEL}")
        _model = SentenceTransformer(EMBEDDING_MODEL)
        print("Embedding model loaded")
    return _model


def embed_sentences(sentences):
    """
    Convert list of sentences to embeddings
    """
    if not sentences:
        return []

    model = get_embedding_model()
    embeddings = model.encode(sentences)

    return embeddings
