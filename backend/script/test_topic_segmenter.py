from backend.pipeline.embedding_generator import EmbeddingGenerator
from backend.pipeline.topic_segmenter import segment_topics

print(">>> test_topic_segmenter STARTED <<<")

sentences = [
    "today we talk about artificial intelligence",
    "machine learning is a subset of ai",
    "deep learning uses neural networks",
    "now let's switch to health and fitness",
    "exercise improves cardiovascular health",
    "nutrition plays an important role"
]

generator = EmbeddingGenerator()
embeddings = generator.generate(sentences)

topics = segment_topics(sentences, embeddings, similarity_threshold=0.6)

for i, topic in enumerate(topics, start=1):
    print(f"\nTopic {i}:")
    for s in topic:
        print("-", s)

print("\n>>> test_topic_segmenter FINISHED <<<")