class SpeechService {
  constructor() {
    this.recognition = null;
    this.synthesis = window.speechSynthesis;
    this.isListening = false;
    
    // Initialize speech recognition if available
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      this.recognition = new SpeechRecognition();
      this.recognition.continuous = true;
      this.recognition.interimResults = true;
      this.recognition.lang = 'en-US';
    }
  }

  isAvailable() {
    return this.recognition !== null;
  }

  startListening(onResult, onEnd, onError) {
    if (!this.recognition) {
      onError(new Error('Speech recognition not available'));
      return;
    }

    this.isListening = true;
    let finalTranscript = '';
    let interimTranscript = '';

    this.recognition.onresult = (event) => {
      interimTranscript = '';
      
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        
        if (event.results[i].isFinal) {
          finalTranscript += transcript + ' ';
        } else {
          interimTranscript += transcript;
        }
      }

      onResult(finalTranscript + interimTranscript, event.results[event.results.length - 1].isFinal);
    };

    this.recognition.onend = () => {
      this.isListening = false;
      onEnd(finalTranscript.trim());
    };

    this.recognition.onerror = (event) => {
      this.isListening = false;
      onError(event.error);
    };

    try {
      this.recognition.start();
    } catch (error) {
      onError(error);
    }
  }

  stopListening() {
    if (this.recognition && this.isListening) {
      this.recognition.stop();
      this.isListening = false;
    }
  }

  speak(text, onEnd) {
    if (!this.synthesis) {
      console.warn('Speech synthesis not available');
      if (onEnd) onEnd();
      return;
    }

    // Cancel any ongoing speech
    this.synthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.9;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;

    if (onEnd) {
      utterance.onend = onEnd;
    }

    this.synthesis.speak(utterance);
  }

  stopSpeaking() {
    if (this.synthesis) {
      this.synthesis.cancel();
    }
  }
}

export default new SpeechService();
