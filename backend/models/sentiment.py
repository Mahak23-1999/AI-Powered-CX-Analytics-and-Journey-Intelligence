from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def predict_sentiment(text):
    score = analyzer.polarity_scores(text)['compound']

    if score >= 0.05:
        label = "positive"
    elif score <= -0.05:
        label = "negative"
    else:
        label = "neutral"

    return {
        "text": text,
        "sentiment": label,
        "score": score
    }