import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# IMPORTANT:
# Run this ONCE separately in a setup script or terminal:
# nltk.download('vader_lexicon')

# Initialize sentiment analyzer once (good practice)
sia = SentimentIntensityAnalyzer()


def get_sentiment(text):
    """
    Returns sentiment label and score for a given text.
    Assumes text is already cleaned in preprocessing step.
    """

    if not text:
        return {
            "text": "",
            "sentiment": "Neutral",
            "score": 0.0
        }

    score = sia.polarity_scores(text)
    compound = score['compound']

    if compound >= 0.05:
        label = "Positive"
    elif compound <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"

    return {
        "text": text,
        "sentiment": label,
        "score": compound
    }