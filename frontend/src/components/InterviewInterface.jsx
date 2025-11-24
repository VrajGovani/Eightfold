import React, { useState, useEffect } from 'react';
import { startInterview, submitAnswer, submitFollowup } from '../services/api';
import { useTimer } from '../hooks/useTimer';
import { useVoiceRecording } from '../hooks/useVoiceRecording';
import speechService from '../services/speechService';

const InterviewInterface = ({ sessionData, onComplete }) => {
  const [loading, setLoading] = useState(true);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [questionNumber, setQuestionNumber] = useState(1);
  const [totalQuestions, setTotalQuestions] = useState(5);
  const [answer, setAnswer] = useState('');
  const [stage, setStage] = useState('prep'); // prep, answer, followup
  const [followupQuestion, setFollowupQuestion] = useState(null);
  const [error, setError] = useState(null);
  const [useVoice, setUseVoice] = useState(false);
  const [answerStartTime, setAnswerStartTime] = useState(null);
  const [selectedRole, setSelectedRole] = useState('');
  const [showRoleSelection, setShowRoleSelection] = useState(true);

  const { isRecording, transcript, startRecording, stopRecording, clearTranscript } = useVoiceRecording();

  // Prep timer (30 seconds)
  const prepTimer = useTimer(30, () => {
    setStage('answer');
    answerTimer.reset(180); // Reset answer timer to 3 minutes
    answerTimer.start();
    setAnswerStartTime(Date.now());
    
    // Speak the question if voice is enabled
    if (useVoice) {
      speechService.speak(currentQuestion.question_text);
    }
  });

  // Answer timer (3 minutes)
  const answerTimer = useTimer(180, () => {
    handleSubmitAnswer(true); // Auto-submit when time runs out
  });

  // Update answer from voice transcript
  useEffect(() => {
    if (transcript) {
      setAnswer(transcript);
    }
  }, [transcript]);

  // Start interview on mount
  useEffect(() => {
    const initInterview = async () => {
      if (!showRoleSelection && selectedRole) {
        try {
          const response = await startInterview(sessionData.session_id, selectedRole);
          setCurrentQuestion(response.question);
          setQuestionNumber(response.question_number);
          setTotalQuestions(response.total_questions);
          
          // Start prep timer
          prepTimer.start();
          setLoading(false);

          // Speak question if voice is enabled
          if (useVoice) {
            speechService.speak(`Question ${response.question_number}: ${response.question.question_text}`);
          }
        } catch (err) {
          setError('Failed to start interview. Please try again.');
          setLoading(false);
        }
      }
    };

    initInterview();
  }, [sessionData, selectedRole, showRoleSelection]);

  const handleRoleSelection = (role) => {
    setSelectedRole(role);
    setShowRoleSelection(false);
  };

  const handleToggleVoice = () => {
    if (isRecording) {
      stopRecording();
    }
    setUseVoice(!useVoice);
  };

  const handleStartVoiceRecording = () => {
    clearTranscript();
    startRecording();
  };

  const handleStopVoiceRecording = () => {
    stopRecording();
  };

  const handleSubmitAnswer = async (autoSubmit = false) => {
    if (!answer.trim() && !autoSubmit) {
      setError('Please provide an answer before submitting.');
      return;
    }

    const duration = answerStartTime ? (Date.now() - answerStartTime) / 1000 : 0;

    setLoading(true);
    answerTimer.pause();

    try {
      const response = await submitAnswer(
        sessionData.session_id,
        currentQuestion.question_id,
        answer.trim() || '(No answer provided)',
        duration,
        useVoice
      );

      if (response.is_interview_complete) {
        onComplete();
      } else if (response.follow_up_question) {
        // Handle follow-up question
        setFollowupQuestion(response.follow_up_question);
        setStage('followup');
        setAnswer('');
        clearTranscript();
        answerTimer.reset(180);
        answerTimer.start();
        setAnswerStartTime(Date.now());

        if (useVoice) {
          speechService.speak(response.follow_up_question.text);
        }
      } else if (response.next_question) {
        // Move to next question
        setCurrentQuestion(response.next_question);
        setQuestionNumber(prev => prev + 1);
        setAnswer('');
        clearTranscript();
        setStage('prep');
        setFollowupQuestion(null);
        prepTimer.reset(30);
        prepTimer.start();

        if (useVoice) {
          speechService.speak(`Next question: ${response.next_question.question_text}`);
        }
      }

      setLoading(false);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit answer. Please try again.');
      setLoading(false);
    }
  };

  const handleSubmitFollowup = async () => {
    if (!answer.trim()) {
      setError('Please provide an answer to the follow-up question.');
      return;
    }

    const duration = answerStartTime ? (Date.now() - answerStartTime) / 1000 : 0;

    setLoading(true);
    answerTimer.pause();

    try {
      const response = await submitFollowup(
        sessionData.session_id,
        currentQuestion.question_id,
        answer.trim(),
        duration
      );

      if (response.is_interview_complete) {
        onComplete();
      } else if (response.next_question) {
        setCurrentQuestion(response.next_question);
        setQuestionNumber(prev => prev + 1);
        setAnswer('');
        clearTranscript();
        setStage('prep');
        setFollowupQuestion(null);
        prepTimer.reset(30);
        prepTimer.start();

        if (useVoice) {
          speechService.speak(`Next question: ${response.next_question.question_text}`);
        }
      }

      setLoading(false);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit follow-up answer.');
      setLoading(false);
    }
  };

  if (showRoleSelection && sessionData.detected_roles) {
    return (
      <div className="interview-interface">
        <h2>Select Interview Role</h2>
        <p style={{ textAlign: 'center', marginBottom: '2rem' }}>
          Based on your resume, we've identified these suitable roles:
        </p>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', maxWidth: '500px', margin: '0 auto' }}>
          {sessionData.detected_roles.map((role, index) => (
            <button
              key={index}
              className="submit-button"
              onClick={() => handleRoleSelection(role)}
            >
              {role}
            </button>
          ))}
        </div>
      </div>
    );
  }

  if (loading && !currentQuestion) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Preparing your personalized interview...</p>
      </div>
    );
  }

  return (
    <div className="interview-interface">
      <div className="interview-header">
        <div>
          <h2>Interview in Progress</h2>
          <p style={{ color: '#7f8c8d' }}>Role: {selectedRole}</p>
        </div>
        <div className="question-progress">
          Question {questionNumber} of {totalQuestions}
        </div>
      </div>

      {error && (
        <div className="error-message">
          ⚠️ {error}
        </div>
      )}

      {currentQuestion && (
        <div className="question-card">
          <div className="question-text">
            {followupQuestion ? (
              <>
                <strong>Follow-up:</strong> {followupQuestion.text}
                <p style={{ fontSize: '0.9rem', color: '#7f8c8d', marginTop: '0.5rem' }}>
                  Reason: {followupQuestion.reason}
                </p>
              </>
            ) : (
              currentQuestion.question_text
            )}
          </div>
        </div>
      )}

      <div className="timer-container">
        {stage === 'prep' && (
          <div className="timer">
            <div className="timer-label">Preparation Time</div>
            <div className={`timer-value ${prepTimer.seconds <= 10 ? 'warning' : ''}`}>
              {prepTimer.formatTime()}
            </div>
          </div>
        )}

        {(stage === 'answer' || stage === 'followup') && (
          <div className="timer">
            <div className="timer-label">Answer Time Remaining</div>
            <div className={`timer-value ${answerTimer.seconds <= 30 ? 'danger' : answerTimer.seconds <= 60 ? 'warning' : ''}`}>
              {answerTimer.formatTime()}
            </div>
          </div>
        )}
      </div>

      {stage === 'prep' && (
        <div style={{ textAlign: 'center', padding: '2rem' }}>
          <p style={{ fontSize: '1.2rem', color: '#2c3e50' }}>
            ⏱️ Take your time to think about your answer...
          </p>
          <p style={{ color: '#7f8c8d', marginTop: '1rem' }}>
            The answer phase will begin automatically when the timer ends.
          </p>
        </div>
      )}

      {(stage === 'answer' || stage === 'followup') && (
        <>
          <div className="answer-area">
            <label>
              <input
                type="checkbox"
                checked={useVoice}
                onChange={handleToggleVoice}
              />
              {' '}Use voice input
            </label>

            {useVoice ? (
              <div className="voice-controls">
                <button
                  className={`voice-button ${isRecording ? 'recording' : ''}`}
                  onClick={isRecording ? handleStopVoiceRecording : handleStartVoiceRecording}
                >
                  {isRecording ? '⏹️ Stop Recording' : '🎤 Start Recording'}
                </button>
              </div>
            ) : null}

            <textarea
              className="answer-textarea"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder="Type your answer here... or use voice recording"
              disabled={loading}
            />

            <p style={{ textAlign: 'right', color: '#7f8c8d', fontSize: '0.9rem', marginTop: '0.5rem' }}>
              Word count: {answer.split(/\s+/).filter(w => w).length}
            </p>
          </div>

          <button
            className="submit-button"
            onClick={followupQuestion ? handleSubmitFollowup : handleSubmitAnswer}
            disabled={loading || (!answer.trim() && !isRecording)}
          >
            {loading ? '⏳ Processing...' : '✓ Submit Answer'}
          </button>
        </>
      )}
    </div>
  );
};

export default InterviewInterface;
