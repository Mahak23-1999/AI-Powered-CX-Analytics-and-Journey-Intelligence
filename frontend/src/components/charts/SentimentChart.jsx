import SentimentChart from "../charts/SentimentChart";
function SentimentChart({ feedbackList }) {
  const positive = feedbackList.filter(f => f.sentiment === 'positive').length;
  const negative = feedbackList.filter(f => f.sentiment === 'negative').length;
  const neutral = feedbackList.filter(f => f.sentiment === 'neutral').length;
  
  const total = feedbackList.length;
  
  const positivePercent = (positive / total) * 100;
  const negativePercent = (negative / total) * 100;
  const neutralPercent = (neutral / total) * 100;

  return (
    <div className="sentiment-chart">
      {/* Pie Chart Using SVG */}
      <div className="chart-container">
        <svg viewBox="0 0 200 200" className="pie-chart">
          {/* Positive Segment */}
          {positive > 0 && (
            <circle
              cx="100"
              cy="100"
              r="80"
              fill="none"
              stroke="#10b981"
              strokeWidth="40"
              strokeDasharray={`${(positivePercent / 100) * 502.4} 502.4`}
              strokeDashoffset="0"
              transform="rotate(-90 100 100)"
            />
          )}
          {/* Negative Segment */}
          {negative > 0 && (
            <circle
              cx="100"
              cy="100"
              r="80"
              fill="none"
              stroke="#ef4444"
              strokeWidth="40"
              strokeDasharray={`${(negativePercent / 100) * 502.4} 502.4`}
              strokeDashoffset={`${-((positivePercent / 100) * 502.4)}`}
              transform="rotate(-90 100 100)"
            />
          )}
          {/* Neutral Segment */}
          {neutral > 0 && (
            <circle
              cx="100"
              cy="100"
              r="80"
              fill="none"
              stroke="#6b7280"
              strokeWidth="40"
              strokeDasharray={`${(neutralPercent / 100) * 502.4} 502.4`}
              strokeDashoffset={`${-((positivePercent + negativePercent) / 100) * 502.4}`}
              transform="rotate(-90 100 100)"
            />
          )}
        </svg>
        <div className="chart-center">
          <p className="center-number">{total}</p>
          <p className="center-label">total</p>
        </div>
      </div>

      {/* Legend */}
      <div className="chart-legend">
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#10b981' }}></span>
          <span className="legend-text">Positive: {positive}</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#ef4444' }}></span>
          <span className="legend-text">Negative: {negative}</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#6b7280' }}></span>
          <span className="legend-text">Neutral: {neutral}</span>
        </div>
      </div>
    </div>
  );
}

export default SentimentChart;