import { useMemo } from "react";
import SentimentChart from "../charts/SentimentChart";
import "./Dashboard.css";

function Dashboard({ feedbackList }) {
  const metrics = useMemo(() => {
    if (feedbackList.length === 0) {
      return {
        total: 0,
        positive: 0,
        negative: 0,
        neutral: 0,
        avgRating: 0,
        positivePercent: 0,
        negativePercent: 0
      };
    }

    const total = feedbackList.length;
    const positive = feedbackList.filter(f => f.sentiment === 'positive').length;
    const negative = feedbackList.filter(f => f.sentiment === 'negative').length;
    const neutral = feedbackList.filter(f => f.sentiment === 'neutral').length;
    const avgRating = (feedbackList.reduce((sum, f) => sum + f.rating, 0) / total).toFixed(1);
    const positivePercent = Math.round((positive / total) * 100);
    const negativePercent = Math.round((negative / total) * 100);

    return {
      total,
      positive,
      negative,
      neutral,
      avgRating,
      positivePercent,
      negativePercent
    };
  }, [feedbackList]);

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Analytics Dashboard</h2>
        <p>Customer Experience Metrics & Insights</p>
      </div>

      {/* Metrics Grid */}
      <div className="metrics-grid">
        {/* Total Feedback */}
        <div className="metric-card metric-total">
          <div className="metric-icon">📊</div>
          <div className="metric-content">
            <h3>Total Feedback</h3>
            <p className="metric-value">{metrics.total}</p>
            <span className="metric-label">submissions</span>
          </div>
        </div>

        {/* Positive */}
        <div className="metric-card metric-positive">
          <div className="metric-icon">😊</div>
          <div className="metric-content">
            <h3>Positive</h3>
            <p className="metric-value">{metrics.positive}</p>
            <span className="metric-label">{metrics.positivePercent}% of total</span>
          </div>
        </div>

        {/* Negative */}
        <div className="metric-card metric-negative">
          <div className="metric-icon">😞</div>
          <div className="metric-content">
            <h3>Negative</h3>
            <p className="metric-value">{metrics.negative}</p>
            <span className="metric-label">{metrics.negativePercent}% of total</span>
          </div>
        </div>

        {/* Average Rating */}
        <div className="metric-card metric-rating">
          <div className="metric-icon">⭐</div>
          <div className="metric-content">
            <h3>Avg Rating</h3>
            <p className="metric-value">{metrics.avgRating}</p>
            <span className="metric-label">out of 10</span>
          </div>
        </div>
      </div>

      {/* Chart Section */}
      {feedbackList.length > 0 && (
        <div className="chart-section">
          <h3>Sentiment Distribution</h3>
          <SentimentChart feedbackList={feedbackList} />
        </div>
      )}

      {/* Empty State */}
      {feedbackList.length === 0 && (
        <div className="empty-state">
          <div className="empty-icon">📝</div>
          <h3>No feedback yet</h3>
          <p>Submit your first feedback to see analytics</p>
        </div>
      )}
    </div>
  );
}

export default Dashboard;