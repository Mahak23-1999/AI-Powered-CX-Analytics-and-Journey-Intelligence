import sys
import os
from flask import Flask, request, jsonify

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ✅ Fixed: was backend.models.sentiment_analysis (models folder doesn't exist)
from backend.sentiment_analysis import get_sentiment

app = Flask(__name__)

@app.route("/")
def home():
    return "CX AI Platform is running!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    review = data.get("review")

    result = get_sentiment(review)

    return jsonify({
        "review": review,
        "sentiment": result["sentiment"],
        "score": result["score"]
    })

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)