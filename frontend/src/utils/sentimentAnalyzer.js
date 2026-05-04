// Basic Rule-Based Sentiment Analyzer
// No ML required - simple keyword matching

const POSITIVE_KEYWORDS = [
  'great', 'excellent', 'amazing', 'wonderful', 'love', 'awesome',
  'fantastic', 'brilliant', 'perfect', 'good', 'nice', 'happy',
  'satisfied', 'impressed', 'best', 'outstanding', 'superb',
  'delighted', 'thrilled', 'wonderful', 'excellent', 'satisfied'
];

const NEGATIVE_KEYWORDS = [
  'terrible', 'awful', 'bad', 'horrible', 'hate', 'worst',
  'disappointing', 'poor', 'angry', 'frustrated', 'upset',
  'annoyed', 'regret', 'waste', 'useless', 'pathetic',
  'disgusting', 'unacceptable', 'broken', 'fail', 'failed'
];

export const analyzeSentiment = (text) => {
  if (!text || typeof text !== 'string') {
    return { sentiment: 'neutral', score: 0 };
  }

  const lowerText = text.toLowerCase();
  
  // Count matches
  let positiveCount = 0;
  let negativeCount = 0;

  POSITIVE_KEYWORDS.forEach(keyword => {
    const regex = new RegExp(`\\b${keyword}\\b`, 'g');
    positiveCount += (lowerText.match(regex) || []).length;
  });

  NEGATIVE_KEYWORDS.forEach(keyword => {
    const regex = new RegExp(`\\b${keyword}\\b`, 'g');
    negativeCount += (lowerText.match(regex) || []).length;
  });

  // Determine sentiment
  if (positiveCount > negativeCount) {
    return { sentiment: 'positive', score: positiveCount };
  } else if (negativeCount > positiveCount) {
    return { sentiment: 'negative', score: negativeCount };
  } else {
    return { sentiment: 'neutral', score: 0 };
  }
};

export const getSentimentColor = (sentiment) => {
  const colors = {
    positive: '#10b981',
    negative: '#ef4444',
    neutral: '#6b7280'
  };
  return colors[sentiment] || colors.neutral;
};