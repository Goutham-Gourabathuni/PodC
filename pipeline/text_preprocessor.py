from nltk.tokenize import sent_tokenize
import nltk

for tokenizer in ("punkt", "punkt_tab"):
    try:
        nltk.data.find(f"tokenizers/{tokenizer}")
    except LookupError:
        nltk.download(tokenizer, quiet=True)


def segment_into_sentences(transcript):
    """
    Accepts Whisper transcript output and extracts sentences safely
    """

    sentences = []

    for seg in transcript:
        # ✅ handle both dict and string
        if isinstance(seg, dict):
            text = seg.get("text", "")
        elif isinstance(seg, str):
            text = seg
        else:
            continue

        text = text.strip()
        if not text:
            continue

        for sent in sent_tokenize(text):
            cleaned = sent.strip()
            if cleaned:
                sentences.append(cleaned)

    return sentences
