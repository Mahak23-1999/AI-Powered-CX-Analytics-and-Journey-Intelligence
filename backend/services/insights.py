from collections import Counter

def generate_insights(results):

    sentiments = [r['sentiment'] for r in results]

    total = len(sentiments)

    summary = {
        "positive": sentiments.count("positive") / total * 100,
        "negative": sentiments.count("negative") / total * 100,
        "neutral": sentiments.count("neutral") / total * 100
    }

    # Extract negative texts for issue detection
    negative_texts = [
        r['text'] for r in results if r['sentiment'] == "negative"
    ]

    words = " ".join(negative_texts).split()
    common_issues = Counter(words).most_common(5)

    return {
        "summary": summary,
        "top_issues": [word for word, _ in common_issues]
    }