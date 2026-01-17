from backend.pipeline.topic_labeler import label_topic

print(">>> test_topic_labeler STARTED <<<")

topic_sentences = [
    "machine learning is a subset of ai",
    "deep learning uses neural networks",
    "artificial intelligence is transforming industries"
]

label = label_topic(topic_sentences)

print("Topic label:", label)

print(">>> test_topic_labeler FINISHED <<<")