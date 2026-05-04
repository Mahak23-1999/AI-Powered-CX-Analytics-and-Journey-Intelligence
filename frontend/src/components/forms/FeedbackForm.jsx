import { useState } from 'react';
import { analyzeSentiment } from "../../utils/sentimentAnalyzer";
import "./FeedbackForm.css";

function FeedbackForm({ onSubmit }) {
  const [text, setText] = useState('');
  const [rating, setRating] = useState(5);
  const [sentiment, setSentiment] = useState(null);

  const handleTextChange = (e) => {
    const newText = e.target.value;
    setText(newText);
    // Real-time sentiment preview
    if (newText.trim()) {
      setSentiment(analyzeSentiment(newText));
    } else {
      setSentiment(null);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!text.trim()) {
      alert('Please enter feedback text');
      return;
    }

    const analysis = analyzeSentiment(text);
    
    onSubmit({
      text,
      rating: parseInt(rating),
      sentiment: analysis.sentiment,
      sentimentScore: analysis.score
    });

    // Reset form
    setText('');
    setRating(5);
    setSentiment(null);
  };

  return (
    <div className="feedback-form-container">
      <div className="form-header">
        <h2>Share Your Experience</h2>
        <p>Help us improve by sharing your feedback</p>
      </div>

      <form className="feedback-form" onSubmit={handleSubmit}>
        {/* Feedback Text Area */}
        <div className="form-group">
          <label htmlFor="feedback-text">Your Feedback *</label>
          <textarea
            id="feedback-text"
            placeholder="Tell us what you think... (e.g., 'Great service, very satisfied with the product!')"
            value={text}
            onChange={handleTextChange}
            rows="6"
            required
          />
          <div className="char-count">{text.length} characters</div>
        </div>

        {/* Real-time Sentiment Preview */}
        {sentiment && (
          <div className={`sentiment-preview sentiment-${sentiment.sentiment}`}>
            <span className="sentiment-icon">
              {sentiment.sentiment === 'positive' && '😊'}
              {sentiment.sentiment === 'negative' && '😞'}
              {sentiment.sentiment === 'neutral' && '😐'}
            </span>
            <span className="sentiment-text">
              Detected: <strong>{sentiment.sentiment.toUpperCase()}</strong>
            </span>
          </div>
        )}

        {/* Rating Slider */}
        <div className="form-group">
          <label htmlFor="rating">Rating: <span className="rating-value">{rating}/10</span></label>
          <input
            id="rating"
            type="range"
            min="1"
            max="10"
            value={rating}
            onChange={(e) => setRating(e.target.value)}
            className="rating-slider"
          />
          <div className="rating-labels">
            <span>Poor</span>
            <span>Average</span>
            <span>Excellent</span>
          </div>
        </div>

        {/* Submit Button */}
        <button type="submit" className="submit-btn">
          ✓ Submit Feedback
        </button>
      </form>
    </div>
  );
}

export default FeedbackForm;