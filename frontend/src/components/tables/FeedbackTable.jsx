import "./FeedbackTable.css";

function FeedbackTable({ feedbackList, onDelete }) {
  if (feedbackList.length === 0) {
    return null;
  }

  return (
    <div className="feedback-table-container">
      <div className="table-header">
        <h3>Recent Feedback</h3>
        <p>{feedbackList.length} submissions</p>
      </div>

      <div className="table-wrapper">
        <table className="feedback-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Feedback</th>
              <th>Sentiment</th>
              <th>Rating</th>
              <th>Date</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {feedbackList.map((feedback, index) => (
              <tr key={feedback.id} className={`sentiment-${feedback.sentiment}`}>
                <td className="index-cell">{index + 1}</td>
                <td className="feedback-cell">
                  <p className="feedback-text">{feedback.text}</p>
                </td>
                <td className="sentiment-cell">
                  <span className={`sentiment-badge sentiment-${feedback.sentiment}`}>
                    {feedback.sentiment === 'positive' && '😊 Positive'}
                    {feedback.sentiment === 'negative' && '😞 Negative'}
                    {feedback.sentiment === 'neutral' && '😐 Neutral'}
                  </span>
                </td>
                <td className="rating-cell">
                  <span className="rating-stars">
                    {'⭐'.repeat(Math.round(feedback.rating / 2))}
                  </span>
                  <span className="rating-number">{feedback.rating}/10</span>
                </td>
                <td className="date-cell">{feedback.timestamp}</td>
                <td className="action-cell">
                  <button
                    className="delete-btn"
                    onClick={() => {
                      if (window.confirm('Delete this feedback?')) {
                        onDelete(feedback.id);
                      }
                    }}
                    title="Delete feedback"
                  >
                    🗑️
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default FeedbackTable;