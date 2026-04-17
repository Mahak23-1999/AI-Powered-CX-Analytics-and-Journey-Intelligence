import sys
import os
from flask import Flask, request, jsonify

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.sentiment_analysis import get_sentiment

app = Flask(__name__)

@app.route("/")
def home():
    return "CX AI Platform is running!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    review = data.get("review")

    sentiment = get_sentiment(review)

    return jsonify({
        "review": review,
        "sentiment": sentiment
    })
if __name__ == "__main__":
    app.run(debug=True)