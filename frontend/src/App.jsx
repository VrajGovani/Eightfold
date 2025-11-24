import React, { useState } from 'react';
import './App.css';
import ResumeUpload from './components/ResumeUpload';
import InterviewInterface from './components/InterviewInterface';
import ReportViewer from './components/ReportViewer';

function App() {
  const [stage, setStage] = useState('upload'); // upload, interview, report
  const [sessionData, setSessionData] = useState(null);
  const [reportData, setReportData] = useState(null);

  const handleResumeUploaded = (data) => {
    setSessionData(data);
    setStage('interview');
  };

  const handleInterviewComplete = () => {
    setStage('report');
  };

  const handleStartOver = () => {
    setStage('upload');
    setSessionData(null);
    setReportData(null);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎯 Interview Practice Partner</h1>
        <p>AI-Powered Mock Interview System</p>
      </header>

      <main className="App-main">
        {stage === 'upload' && (
          <ResumeUpload onResumeUploaded={handleResumeUploaded} />
        )}

        {stage === 'interview' && sessionData && (
          <InterviewInterface
            sessionData={sessionData}
            onComplete={handleInterviewComplete}
          />
        )}

        {stage === 'report' && sessionData && (
          <ReportViewer
            sessionId={sessionData.session_id}
            onStartOver={handleStartOver}
          />
        )}
      </main>

      <footer className="App-footer">
        <p>Built with Intelligence • Mahesh-Level Mindset • Production-Ready</p>
      </footer>
    </div>
  );
}

export default App;
