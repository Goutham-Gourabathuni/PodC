print(">>> test_text_preprocessor STARTED <<<")

from backend.pipeline.text_preprocessor import preprocess_text

raw_text = """
The birch canoes slid on the smooth planks.
Glue the sheet to the dark blue background.
It is easy to tell the depth of a well.
"""

sentences = preprocess_text(raw_text)

print("Processed sentences:")
for s in sentences:
    print("-", s)

print(">>> test_text_preprocessor FINISHED <<<")