import React, { useState, useEffect } from 'react';
import { generateReport, downloadPDF } from '../services/api';

const ReportViewer = ({ sessionId, onStartOver }) => {
  const [loading, setLoading] = useState(true);
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const reportData = await generateReport(sessionId, 'json');
        setReport(reportData.json_report || reportData);
        setLoading(false);
      } catch (err) {
        setError('Failed to generate report. Please try again.');
        setLoading(false);
      }
    };

    fetchReport();
  }, [sessionId]);

  const handleDownloadPDF = async () => {
    try {
      const blob = await downloadPDF(sessionId);
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `interview_report_${sessionId}.pdf`;
      link.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert('Failed to download PDF. Please try again.');
    }
  };

  const handleDownloadJSON = () => {
    const dataStr = JSON.stringify(report, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `interview_report_${sessionId}.json`;
    link.click();
    window.URL.revokeObjectURL(url);
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Generating your performance report...</p>
      </div>
    );
  }

  if (error || !report) {
    return (
      <div className="report-viewer">
        <div className="error-message">{error || 'No report data available.'}</div>
        <button className="start-over-button" onClick={onStartOver}>
          Start Over
        </button>
      </div>
    );
  }

  const getScoreColor = (score) => {
    if (score >= 75) return '#28a745';
    if (score >= 60) return '#ffc107';
    return '#dc3545';
  };

  const getRecommendationEmoji = (level) => {
    if (level === 'Strong') return '🌟';
    if (level === 'Intermediate') return '👍';
    return '📚';
  };

  return (
    <div className="report-viewer">
      <div className="report-header">
        <h2>🎉 Interview Complete!</h2>
        <p style={{ color: '#7f8c8d' }}>Here's your comprehensive performance report</p>
      </div>

      <div className="score-card">
        <h3>Overall Performance</h3>
        <div className="overall-score">{report.scores.overall}/100</div>
        <div className="recommendation">
          {getRecommendationEmoji(report.recommendation_level)} {report.recommendation_level} Candidate
        </div>
        <div style={{ marginTop: '1rem', fontSize: '1.1rem' }}>
          {report.ready_for_interviews ? '✅ Ready for Interviews' : '⏳ Needs More Practice'}
        </div>
      </div>

      <div className="score-breakdown">
        <div className="score-item">
          <div className="score-item-label">Confidence</div>
          <div className="score-item-value" style={{ color: getScoreColor(report.scores.confidence) }}>
            {report.scores.confidence}
          </div>
        </div>
        <div className="score-item">
          <div className="score-item-label">Communication</div>
          <div className="score-item-value" style={{ color: getScoreColor(report.scores.communication) }}>
            {report.scores.communication}
          </div>
        </div>
        <div className="score-item">
          <div className="score-item-label">Technical Depth</div>
          <div className="score-item-value" style={{ color: getScoreColor(report.scores.technical_depth) }}>
            {report.scores.technical_depth}
          </div>
        </div>
        <div className="score-item">
          <div className="score-item-label">STAR Method</div>
          <div className="score-item-value" style={{ color: getScoreColor(report.scores.star_method_usage) }}>
            {report.scores.star_method_usage}
          </div>
        </div>
        <div className="score-item">
          <div className="score-item-label">Behavioral Clarity</div>
          <div className="score-item-value" style={{ color: getScoreColor(report.scores.behavioral_clarity) }}>
            {report.scores.behavioral_clarity}
          </div>
        </div>
      </div>

      <div className="report-section">
        <h3>💪 Your Strengths</h3>
        <ul className="report-list">
          {report.overall_strengths.map((strength, index) => (
            <li key={index}>{strength}</li>
          ))}
        </ul>
      </div>

      <div className="report-section">
        <h3>📈 Areas for Improvement</h3>
        <ul className="report-list">
          {report.overall_weaknesses.map((weakness, index) => (
            <li key={index}>{weakness}</li>
          ))}
        </ul>
      </div>

      <div className="report-section">
        <h3>💡 Improvement Suggestions</h3>
        <ul className="report-list">
          {report.improvement_suggestions.map((suggestion, index) => (
            <li key={index}>{suggestion}</li>
          ))}
        </ul>
      </div>

      <div className="report-section">
        <h3>🎯 Recommended Next Steps</h3>
        <ul className="report-list">
          {report.recommended_next_steps.map((step, index) => (
            <li key={index}>{step}</li>
          ))}
        </ul>
      </div>

      <div className="report-section">
        <h3>📊 Interview Analytics</h3>
        <div style={{ background: '#f8f9fa', padding: '1.5rem', borderRadius: '8px' }}>
          <p><strong>Duration:</strong> {report.duration_minutes.toFixed(1)} minutes</p>
          <p><strong>Communication Style:</strong> {report.communication_style}</p>
          <p><strong>STAR Method Consistency:</strong> {report.star_method_consistency}</p>
          <p><strong>Dominant Persona:</strong> {report.dominant_persona}</p>
        </div>
      </div>

      <div className="download-buttons">
        <button className="download-button" onClick={handleDownloadPDF}>
          📄 Download PDF Report
        </button>
        <button className="download-button" onClick={handleDownloadJSON}>
          📊 Download JSON Data
        </button>
      </div>

      <button className="start-over-button" onClick={onStartOver}>
        🔄 Start New Interview
      </button>
    </div>
  );
};

export default ReportViewer;
