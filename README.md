# Interview Practice Partner - AI-Powered Mock Interview System

> 🎯 **Live Demo:** [http://localhost:3001](http://localhost:3001) (after local setup)  
> 📦 **Repository:** [https://github.com/VrajGovani/Eightfold](https://github.com/VrajGovani/Eightfold)

A full-stack intelligent interview practice system that conducts realistic mock job interviews based on uploaded resumes, provides real-time feedback, and generates comprehensive performance reports with PDF export.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.2-61DAFB.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Features

### Core Capabilities
- **📄 Resume-Based Dynamic Interviews**: Upload PDF/DOCX/TXT resumes for personalized questions targeting **internships, projects, and experience**
- **🎤 Voice & Chat Interface**: Real-time voice interaction with Web Speech API + text fallback
- **🤖 Intelligent Follow-ups**: Context-aware probing questions based on response quality
- **👥 Persona Detection**: Adapts to confused, efficient, chatty, or edge-case users
- **⏱️ Timer Management**: 30-second prep time + 3-minute answer windows with auto-submit
- **⭐ STAR Method Evaluation**: Real-time detection of Situation, Task, Action, Result
- **📊 Comprehensive Reports**: PDF/JSON export with scores, breakdowns, and actionable feedback
- **🎯 Multi-Role Support**: Technical (Software Engineer, Data Analyst, Data Engineer) + Non-Technical (Project Manager, Business Analyst, Marketing Manager, HR Manager)

### Intelligent Behaviors (Production-Ready)
- ✅ Detects irrelevant/off-topic answers and politely redirects
- ✅ Asks deeper probing questions referencing **specific projects and internships**
- ✅ Provides hints when users struggle
- ✅ Challenges highly confident users with follow-up questions
- ✅ Handles edge cases: invalid inputs, nonsense text, overly long answers
- ✅ Adapts questioning style based on detected user persona

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React)                        │
│  • Resume Upload  • Voice Recording  • Timer Display        │
│  • Chat Interface • Report Viewer                           │
└──────────────────────┬──────────────────────────────────────┘
                       │ REST API
┌──────────────────────▼──────────────────────────────────────┐
│                   Backend (FastAPI)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              LLM Agent Architecture                   │  │
│  │                                                        │  │
│  │  • ResumeParser         • InterviewQuestionGenerator  │  │
│  │  • FollowUpEngine       • ResponseEvaluator           │  │
│  │  • PersonaDetector      • STARPatternChecker          │  │
│  │  • ReportGenerator      • ContextMemoryManager        │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
interview-practice-partner/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── config.py               # Configuration management
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── resume.py           # Resume data models
│   │   │   ├── interview.py        # Interview session models
│   │   │   └── report.py           # Report models
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── resume_parser.py    # Resume extraction
│   │   │   ├── question_generator.py # Dynamic question creation
│   │   │   ├── followup_engine.py  # Context-aware follow-ups
│   │   │   ├── response_evaluator.py # Answer analysis
│   │   │   ├── persona_detector.py # User behavior detection
│   │   │   ├── star_checker.py     # STAR method detection
│   │   │   └── report_generator.py # Final report creation
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── interview_service.py # Core interview logic
│   │   │   ├── pdf_service.py      # PDF generation
│   │   │   └── llm_service.py      # LLM integration
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py           # API endpoints
│   │   │   └── websocket.py        # Real-time communication
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── file_parser.py      # Resume file handling
│   │       ├── logger.py           # Logging configuration
│   │       └── validators.py       # Input validation
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_resume_parser.py
│   │   ├── test_interview_logic.py
│   │   ├── test_persona_detector.py
│   │   ├── test_star_checker.py
│   │   └── sample_resume.pdf
│   ├── requirements.txt
│   └── pytest.ini
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/
│   │   ├── components/
│   │   │   ├── ResumeUpload.jsx
│   │   │   ├── InterviewInterface.jsx
│   │   │   ├── Timer.jsx
│   │   │   ├── VoiceRecorder.jsx
│   │   │   ├── ChatBubble.jsx
│   │   │   └── ReportViewer.jsx
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   ├── voiceService.js
│   │   │   └── speechService.js
│   │   ├── hooks/
│   │   │   ├── useTimer.js
│   │   │   └── useVoiceRecording.js
│   │   ├── utils/
│   │   │   └── helpers.js
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   └── .env.example
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
├── .env.example
├── .gitignore
└── README.md
```

## 🚀 Setup Instructions

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Docker & Docker Compose (optional)
- OpenAI API key or compatible LLM API

### Local Development

#### 1. Clone and Setup
```bash
git clone <repository-url>
cd interview-practice-partner
```

#### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp ../.env.example .env
# Edit .env with your API keys

# Run backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

#### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with backend URL

# Run frontend
npm start
```

Frontend will be available at: `http://localhost:3000`

### Docker Deployment

```bash
# Build and run all services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🎬 Interview Flow

### Phase 1: Resume Upload & Parsing
1. User uploads resume (PDF/DOCX/TXT)
2. Backend extracts: skills, experience, projects, education
3. System generates 5 customized questions based on role

### Phase 2: Interview Session
For each of 5 questions:
1. **Preparation Phase** (30 seconds)
   - Question displayed/spoken
   - Countdown timer shown
   - User prepares mentally

2. **Answer Phase** (3 minutes max)
   - User responds via voice or chat
   - "Submit Answer" button to finish early
   - Auto-cutoff at 3 minutes

3. **Real-time Analysis**
   - Persona detection (confused/efficient/chatty/edge-case)
   - Response quality evaluation
   - STAR method detection
   - Context memory updated

4. **Intelligent Follow-up** (if needed)
   - Redirect if off-topic
   - Probe deeper on interesting points
   - Provide hints if struggling
   - Challenge if too confident

### Phase 3: Report Generation
After all questions:
- Comprehensive performance analysis
- Confidence score (0-100)
- Communication quality rating
- Technical depth assessment
- STAR method usage
- Behavioral clarity score
- Strengths & weaknesses
- Improvement suggestions
- Overall recommendation: Beginner/Intermediate/Strong

## 🧠 Agent Reasoning Flow

```
┌──────────────────┐
│ Resume Upload    │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ ResumeParser                         │
│ • Extract structured data            │
│ • Identify key skills & projects     │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ InterviewQuestionGenerator           │
│ • Generate 5 role-specific questions │
│ • Prioritize resume highlights       │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ For each question:                   │
│                                      │
│  ┌────────────────────────────────┐ │
│  │ 1. Present Question            │ │
│  │    (30-sec prep timer)         │ │
│  └──────────┬─────────────────────┘ │
│             │                        │
│             ▼                        │
│  ┌────────────────────────────────┐ │
│  │ 2. Capture Response            │ │
│  │    (3-min answer timer)        │ │
│  └──────────┬─────────────────────┘ │
│             │                        │
│             ▼                        │
│  ┌────────────────────────────────┐ │
│  │ 3. PersonaDetector             │ │
│  │    • Confused → Guide          │ │
│  │    • Efficient → Keep crisp    │ │
│  │    • Chatty → Redirect         │ │
│  │    • Edge-case → Handle error  │ │
│  └──────────┬─────────────────────┘ │
│             │                        │
│             ▼                        │
│  ┌────────────────────────────────┐ │
│  │ 4. ResponseEvaluator           │ │
│  │    • Check relevance           │ │
│  │    • Detect STAR pattern       │ │
│  │    • Assess technical depth    │ │
│  │    • Measure confidence        │ │
│  └──────────┬─────────────────────┘ │
│             │                        │
│             ▼                        │
│  ┌────────────────────────────────┐ │
│  │ 5. FollowUpEngine              │ │
│  │    If needed:                  │ │
│  │    • Redirect if off-topic     │ │
│  │    • Probe deeper              │ │
│  │    • Provide hints             │ │
│  │    • Challenge further         │ │
│  └────────────────────────────────┘ │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ ReportGenerator                      │
│ • Aggregate all evaluations          │
│ • Calculate scores                   │
│ • Generate insights                  │
│ • Export PDF/JSON                    │
└──────────────────────────────────────┘
```

## 🎭 Persona Modeling Logic

### Confused User
**Detection Signals:**
- Hesitant language: "um", "I think", "maybe"
- Short, incomplete answers
- Off-topic responses
- Requests for clarification

**System Response:**
- Simplify questions
- Provide hints and examples
- Break down complex topics
- Offer guided mode

### Efficient User
**Detection Signals:**
- Concise, structured answers
- Uses STAR method naturally
- Direct communication
- Completes answers quickly

**System Response:**
- Keep questions crisp
- Reduce explanatory content
- Move through questions faster
- Ask more challenging questions

### Chatty User
**Detection Signals:**
- Very long responses
- Multiple tangents
- Exceeds time limits
- Over-elaborates on simple points

**System Response:**
- Gentle interruptions
- "Let's focus on..."
- Time reminders
- Redirect to core question

### Edge-Case User
**Detection Signals:**
- Nonsense text
- Invalid inputs
- Extremely short answers (< 10 words)
- No response to follow-ups

**System Response:**
- Polite error handling
- Request clarification
- Offer multiple choice options
- Suggest chat over voice

## ⏱️ Timer Implementation

### Preparation Timer (30 seconds)
```javascript
// Frontend countdown display
// Backend tracks start time
// No penalties for prep time
```

### Answer Timer (3 minutes)
```javascript
// Frontend countdown with visual warning
// "Submit Answer" button to finish early
// Backend enforces 3-minute hard limit
// Auto-submission at timeout
```

### Time Compliance Verification
- Frontend sends answer with timestamp
- Backend validates duration
- Logs timing violations (no penalty, just tracking)
- Report includes time management feedback

## 📊 Evaluation Metrics

### Confidence Score (0-100)
- Language certainty: "I believe" vs "I know"
- Use of concrete examples
- Decisiveness in explanations

### Communication Quality (0-100)
- Clarity and structure
- Grammar and articulation
- Logical flow
- Conciseness vs rambling

### Technical Depth (0-100)
- Use of technical terminology
- Explanation of concepts
- Problem-solving approach
- Details and examples

### STAR Method Detection
- **Situation**: Context described
- **Task**: Responsibility identified
- **Action**: Steps taken explained
- **Result**: Outcome quantified

### Behavioral Clarity (0-100)
- Relevance to question
- Specific examples
- Self-awareness
- Professional maturity

## 🚢 Deployment Options

### Option 1: Render
```bash
# Backend: Web Service
# Build Command: pip install -r requirements.txt
# Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT

# Frontend: Static Site
# Build Command: npm run build
# Publish Directory: build
```

### Option 2: Railway
```bash
# Add railway.json for configuration
# Connect GitHub repo
# Auto-deploys on push
```

### Option 3: Vercel (Frontend) + Render (Backend)
```bash
# Frontend on Vercel
vercel --prod

# Backend on Render
# Use Dockerfile.backend
```

### Option 4: AWS/GCP/Azure
```bash
# Use Docker Compose
# Deploy to container service
# Configure load balancer
# Set up environment variables
```

## 🎥 Demo Video Recording Guide

### What to Showcase
1. **Resume Upload** (30 sec)
   - Upload sample resume
   - Show parsing results

2. **Interview Flow** (3 min)
   - Start interview
   - Show prep timer
   - Answer 2-3 questions via voice
   - Demonstrate "Submit Answer" button
   - Show intelligent follow-up

3. **Edge Case Handling** (1 min)
   - Give an off-topic answer
   - Show redirection behavior

4. **Report Generation** (1 min)
   - Complete interview
   - Display comprehensive report
   - Download PDF

5. **Code Walkthrough** (2 min)
   - Show agent architecture
   - Explain persona detection
   - Highlight key features

### Recording Tips
- Use OBS Studio or Loom
- 1080p resolution
- Include voiceover explanation
- Show both UI and terminal logs
- Total length: 7-10 minutes

## 📝 Example Interview Transcript

```
System: Welcome! I've analyzed your resume. You're interviewing for a Software Engineer position. Let's begin.

System: Question 1/5: I see you worked on a microservices project at XYZ Corp. Can you walk me through your architecture decisions?
[30-second prep timer displayed]

User: [After prep] We used Spring Boot for our services and... um... deployed on AWS...

System: You mentioned AWS. Can you be more specific about which AWS services you used and why you chose them over alternatives?

User: We used ECS for container orchestration because it integrated well with our existing AWS infrastructure. We also used RDS for the database and S3 for file storage. The main reason was team familiarity and cost optimization.

System: [Detects STAR pattern: partial] Can you quantify the cost savings or performance improvements?

User: We reduced our infrastructure costs by about 30% compared to our previous EC2-based setup, and deployment times went from 2 hours to 15 minutes.

System: Excellent specificity. [Records: Confidence 78%, Technical Depth 82%, STAR usage detected]

System: Question 2/5: Tell me about a time you had to debug a critical production issue...
[Continues for 5 questions total]

--- After all questions ---

System: Interview complete! Generating your performance report...

REPORT SUMMARY:
Overall Score: 76/100 - Intermediate Candidate
✓ Strong technical depth
✓ Good use of specific examples
⚠ Could improve STAR method structure
⚠ Some hesitation in explanations
💡 Practice quantifying impact more consistently
```

## 🧪 Testing

### Run All Tests
```bash
cd backend
pytest tests/ -v --cov=app
```

### Test Individual Components
```bash
pytest tests/test_resume_parser.py -v
pytest tests/test_persona_detector.py -v
pytest tests/test_star_checker.py -v
```

### Manual Testing
Use `sample_resume.pdf` in tests/ folder for consistent testing.

## 🔑 Environment Variables

### Backend (.env)
```
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key  # Optional
LLM_PROVIDER=openai  # or anthropic, local
LLM_MODEL=gpt-4-turbo-preview
MAX_TOKENS=2000
TEMPERATURE=0.7
ALLOWED_ORIGINS=http://localhost:3000,https://your-domain.com
LOG_LEVEL=INFO
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws
REACT_APP_ENV=development
```

## 🛠️ Technologies Used

### Backend
- **FastAPI**: Modern Python web framework
- **LangChain**: LLM orchestration
- **OpenAI GPT-4**: Language model
- **PyPDF2**: PDF parsing
- **python-docx**: DOCX parsing
- **ReportLab**: PDF generation
- **Pydantic**: Data validation
- **pytest**: Testing framework

### Frontend
- **React 18**: UI framework
- **Web Speech API**: Voice input/output
- **Axios**: HTTP client
- **React Context**: State management
- **CSS3**: Styling

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **GitHub Actions**: CI/CD (optional)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙋 Support

For issues, questions, or suggestions:
- Create a GitHub issue
- Email: support@interviewpractice.ai

## 🎯 Future Enhancements

- [ ] Multi-language support
- [ ] Video interview mode
- [ ] Team interview simulations
- [ ] Industry-specific question banks
- [ ] Integration with job boards
- [ ] Mobile app version
- [ ] Real-time collaboration mode
- [ ] AI interviewer personalities

---

**Built with the Mahesh-level mindset** - Intelligent, adaptive, and production-ready. 🚀
