import { useState } from "react";
import "./App.css";

import FeedbackForm from "./components/forms/FeedbackForm";
import Dashboard from "./components/dashboard/Dashboard";
import FeedbackTable from "./components/tables/FeedbackTable";

function App() {
  const [feedbackList, setFeedbackList] = useState([]);
  const [currentPage, setCurrentPage] = useState('input'); // 'input' or 'dashboard'

  const addFeedback = (feedback) => {
    const newFeedback = {
      id: Date.now(),
      ...feedback,
      timestamp: new Date().toLocaleDateString()
    };
    setFeedbackList([newFeedback, ...feedbackList]);
    // Show success message
    alert('✅ Feedback submitted successfully!');
  };

  const deleteFeedback = (id) => {
    setFeedbackList(feedbackList.filter(item => item.id !== id));
  };

  return (
    <div className="app">
      {/* Navigation */}
      <nav className="navbar">
        <div className="nav-container">
          <div className="nav-brand">
            <h1>📊 CX Analytics</h1>
            <p>Customer Experience Insights</p>
          </div>
          <div className="nav-links">
            <button 
              className={`nav-btn ${currentPage === 'input' ? 'active' : ''}`}
              onClick={() => setCurrentPage('input')}
            >
              ✍️ Submit Feedback
            </button>
            <button 
              className={`nav-btn ${currentPage === 'dashboard' ? 'active' : ''}`}
              onClick={() => setCurrentPage('dashboard')}
            >
              📈 Dashboard
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="main-content">
        {currentPage === 'input' ? (
          <div className="page-container">
            <FeedbackForm onSubmit={addFeedback} />
          </div>
        ) : (
          <div className="page-container">
            <Dashboard feedbackList={feedbackList} />
            <FeedbackTable 
              feedbackList={feedbackList} 
              onDelete={deleteFeedback}
            />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="footer">
        <p>CX Analytics MVP • Built for viva presentation</p>
      </footer>
    </div>
  );
}

export default App;