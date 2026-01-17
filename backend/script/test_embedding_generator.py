from backend.pipeline.embedding_generator import EmbeddingGenerator

sentences = [
    "the birch canoes slid on the smooth planks.",
    "glue the sheet to the dark blue background.",
    "it is easy to tell the depth of a well."
]

generator = EmbeddingGenerator()
embeddings = generator.generate(sentences)

print("Embeddings shape:", embeddings.shape)
print("First embedding vector (truncated):")
print(embeddings[0][:10])