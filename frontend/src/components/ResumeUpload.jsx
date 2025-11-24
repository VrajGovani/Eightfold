import React, { useState } from 'react';
import { uploadResume } from '../services/api';

const ResumeUpload = ({ onResumeUploaded }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [dragging, setDragging] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      validateAndSetFile(selectedFile);
    }
  };

  const validateAndSetFile = (selectedFile) => {
    const validExtensions = ['.pdf', '.docx', '.txt'];
    const fileExtension = '.' + selectedFile.name.split('.').pop().toLowerCase();

    if (!validExtensions.includes(fileExtension)) {
      setError(`Invalid file type. Please upload ${validExtensions.join(', ')} files only.`);
      return;
    }

    if (selectedFile.size > 10 * 1024 * 1024) {
      setError('File size exceeds 10MB limit.');
      return;
    }

    setFile(selectedFile);
    setError(null);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);

    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      validateAndSetFile(droppedFile);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first.');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      console.log('Uploading file:', file.name, 'Size:', file.size);
      const response = await uploadResume(file);
      console.log('Upload response:', response);
      onResumeUploaded(response);
    } catch (err) {
      console.error('Upload error:', err);
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to upload resume. Please try again.';
      setError(errorMessage);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="resume-upload">
      <h2>📄 Upload Your Resume</h2>
      <p style={{ textAlign: 'center', color: '#7f8c8d', marginBottom: '2rem' }}>
        Upload your resume to get personalized interview questions
      </p>

      <div
        className={`upload-area ${dragging ? 'dragging' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => document.getElementById('file-input').click()}
      >
        <div className="upload-icon">📁</div>
        <p style={{ fontSize: '1.1rem', color: '#2c3e50', marginBottom: '0.5rem' }}>
          {file ? file.name : 'Drag & drop your resume here'}
        </p>
        <p style={{ color: '#7f8c8d', fontSize: '0.9rem' }}>
          or click to browse (PDF, DOCX, TXT)
        </p>
        <input
          id="file-input"
          type="file"
          accept=".pdf,.docx,.txt"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
      </div>

      {error && (
        <div className="error-message">
          ⚠️ {error}
        </div>
      )}

      {file && !error && (
        <div className="success-message">
          ✓ File selected: {file.name} ({(file.size / 1024).toFixed(2)} KB)
        </div>
      )}

      <button
        className="upload-button"
        onClick={handleUpload}
        disabled={!file || uploading}
      >
        {uploading ? '⏳ Analyzing Resume...' : '🚀 Start Interview'}
      </button>

      <div style={{ marginTop: '2rem', textAlign: 'center', color: '#7f8c8d', fontSize: '0.9rem' }}>
        <p>✓ Your data is processed securely</p>
        <p>✓ AI-powered resume analysis</p>
        <p>✓ Personalized interview questions</p>
      </div>
    </div>
  );
};

export default ResumeUpload;
