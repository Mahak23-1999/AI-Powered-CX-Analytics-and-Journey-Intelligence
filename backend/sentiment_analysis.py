from textblob import TextBlob


def analyze_sentiment(text):
    """Core sentiment function. Returns dict with 'sentiment' and 'score'."""

    # STEP 1: handle None / NaN / float
    if text is None:
        return {"sentiment": "Neutral", "score": 0.0}

    text = str(text).strip()

    # STEP 2: handle empty or "nan"
    if text == "" or text.lower() == "nan":
        return {"sentiment": "Neutral", "score": 0.0}

    # STEP 3: run TextBlob
    analysis = TextBlob(text)
    polarity = round(analysis.sentiment.polarity, 4)

    # STEP 4: output label
    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {"sentiment": sentiment, "score": polarity}


# Alias so both app.py files can use get_sentiment without changes
get_sentiment = analyze_sentiment