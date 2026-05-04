import re

def clean_text(text):
    if not text:
        return ""

    text = text.lower()                          # lowercase
    text = re.sub(r'[^\w\s]', '', text)          # remove punctuation
    text = re.sub(r'\s+', ' ', text).strip()     # remove extra spaces

    return text