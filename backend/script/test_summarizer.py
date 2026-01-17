print(">>> test_summarizer STARTED <<<")

from backend.pipeline.summarizer import summarize_all_topics
import numpy as np

topics = {
    "Learning Machine Subset": [
        "machine learning is a subset of ai",
        "deep learning uses neural networks",
        "artificial intelligence is transforming industries"
    ],
    "Health Fitness": [
        "exercise improves cardiovascular health",
        "nutrition plays an important role",
        "regular activity boosts mental health"
    ]
}

embeddings_map = {
    "Learning Machine Subset": np.random.rand(3, 384),
    "Health Fitness": np.random.rand(3, 384)
}

summaries = summarize_all_topics(topics, embeddings_map)

print("\n--- SUMMARIES ---")
for topic, summary in summaries.items():
    print(f"\n{topic}:")
    print(summary)

print("\n>>> test_summarizer FINISHED <<<")
