import { useState, useCallback } from 'react';
import speechService from '../services/speechService';

export const useVoiceRecording = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [error, setError] = useState(null);

  const startRecording = useCallback(() => {
    if (!speechService.isAvailable()) {
      setError('Speech recognition is not available in your browser');
      return;
    }

    setIsRecording(true);
    setError(null);
    setTranscript('');

    speechService.startListening(
      (text, isFinal) => {
        setTranscript(text);
      },
      (finalText) => {
        setTranscript(finalText);
        setIsRecording(false);
      },
      (err) => {
        setError(`Recording error: ${err}`);
        setIsRecording(false);
      }
    );
  }, []);

  const stopRecording = useCallback(() => {
    speechService.stopListening();
    setIsRecording(false);
  }, []);

  const clearTranscript = useCallback(() => {
    setTranscript('');
    setError(null);
  }, []);

  return {
    isRecording,
    transcript,
    error,
    startRecording,
    stopRecording,
    clearTranscript,
  };
};
