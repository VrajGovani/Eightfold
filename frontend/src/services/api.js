import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadResume = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    console.log('Uploading to:', `${API_URL}/api/upload-resume`);
    console.log('File:', file.name, file.type, file.size);

    const response = await api.post('/upload-resume', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  } catch (error) {
    console.error('API error:', error.response || error);
    throw error;
  }
};

export const startInterview = async (sessionId, targetRole) => {
  const response = await api.post('/start-interview', {
    session_id: sessionId,
    target_role: targetRole,
  });

  return response.data;
};

export const submitAnswer = async (sessionId, questionId, answerText, durationSeconds, isVoice = false) => {
  const response = await api.post('/submit-answer', {
    session_id: sessionId,
    question_id: questionId,
    answer_text: answerText,
    duration_seconds: durationSeconds,
    is_voice: isVoice,
  });

  return response.data;
};

export const submitFollowup = async (sessionId, questionId, answerText, durationSeconds) => {
  const response = await api.post('/submit-followup', {
    session_id: sessionId,
    question_id: questionId,
    answer_text: answerText,
    duration_seconds: durationSeconds,
  });

  return response.data;
};

export const getSession = async (sessionId) => {
  const response = await api.get(`/session/${sessionId}`);
  return response.data;
};

export const generateReport = async (sessionId, exportFormat = 'json') => {
  const response = await api.post('/generate-report', {
    session_id: sessionId,
    export_format: exportFormat,
  });

  return response.data;
};

export const downloadPDF = async (sessionId) => {
  const response = await api.get(`/download-pdf/${sessionId}`, {
    responseType: 'blob',
  });

  return response.data;
};

export default api;
