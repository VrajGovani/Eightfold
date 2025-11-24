# Demo Video Recording Script

## Preparation (Before Recording)

### Setup
- [ ] Start backend: `cd backend && uvicorn app.main:app --reload`
- [ ] Start frontend: `cd frontend && npm start`
- [ ] Clear browser cache
- [ ] Prepare sample resume (PDF)
- [ ] Set up screen recording (OBS, Loom, QuickTime)
- [ ] Test audio levels
- [ ] Close unnecessary browser tabs
- [ ] Set resolution to 1920x1080

### Sample Resume Content
Create a PDF with:
```
Jane Smith
jane.smith@email.com | (555) 987-6543
linkedin.com/in/janesmith | github.com/janesmith

PROFESSIONAL SUMMARY
Senior Full-Stack Developer with 6+ years building scalable web applications.
Expert in React, Node.js, Python, and cloud technologies.

SKILLS
Frontend: React, TypeScript, Redux, Tailwind CSS
Backend: Node.js, Python, FastAPI, Django
Database: PostgreSQL, MongoDB, Redis
Cloud: AWS (EC2, S3, Lambda), Docker, Kubernetes
Tools: Git, Jenkins, Jira, Postman

EXPERIENCE

Senior Software Engineer | TechCorp Inc | Jan 2021 - Present
• Led development of microservices architecture serving 1M+ users
• Reduced API response time by 60% through optimization
• Mentored team of 5 junior developers
• Technologies: React, Node.js, PostgreSQL, AWS, Docker

Software Engineer | StartupXYZ | Jun 2018 - Dec 2020
• Built REST APIs handling 100K+ requests/day
• Implemented CI/CD pipeline reducing deployment time by 80%
• Developed real-time chat feature using WebSockets
• Technologies: Python, Django, React, Redis

PROJECTS

E-Commerce Platform
• Full-stack application with payment integration
• Built using MERN stack with Stripe API
• Achieved 99.9% uptime with load balancing
• Link: github.com/janesmith/ecommerce

Task Management System
• Real-time collaborative tool for teams
• WebSocket-based updates, JWT authentication
• Deployed on AWS with auto-scaling
• Link: taskmanager-demo.com

EDUCATION
Bachelor of Science in Computer Science
State University | 2014-2018 | GPA: 3.9/4.0
Dean's List, Computer Science Award

CERTIFICATIONS
• AWS Certified Solutions Architect
• Google Cloud Professional
```

---

## Recording Script (10 minutes)

### Part 1: Introduction (0:00 - 1:00)

**[Screen: Application homepage]**

**Script:**
"Welcome to the Interview Practice Partner demo. This is an AI-powered mock interview system that I've built with what I call a 'Mahesh-level mindset' - meaning it's intelligent, adaptive, and production-ready.

The system conducts realistic job interviews based on your resume, provides real-time feedback, and generates comprehensive performance reports. Let me show you how it works."

---

### Part 2: Resume Upload (1:00 - 2:00)

**[Screen: Resume upload page]**

**Actions:**
1. Drag and drop the sample resume PDF
2. Show file validation
3. Click "Start Interview"

**Script:**
"First, you upload your resume. The system accepts PDF, DOCX, and text files. Watch as it parses the resume using an LLM-powered extraction module...

[Wait for parsing]

The system has analyzed Jane's resume and identified her skills, experience, and projects. It's detected that she'd be suitable for roles like Senior Software Engineer, Full-Stack Developer, and Technical Lead.

Let's select Software Engineer for this demo."

---

### Part 3: Interview Flow - Preparation Timer (2:00 - 2:45)

**[Screen: Interview interface with prep timer]**

**Actions:**
1. Select "Software Engineer" role
2. Show the first question appearing
3. Display 30-second preparation timer

**Script:**
"The interview begins with a 30-second preparation timer for each question. This gives you time to think about your answer - just like a real interview.

Notice the question is personalized based on Jane's resume - it specifically asks about her microservices experience at TechCorp.

The timer is counting down... and when it reaches zero, the answer phase will begin automatically."

---

### Part 4: Answering with Voice (2:45 - 4:30)

**[Screen: Answer phase with timer]**

**Actions:**
1. Show 3-minute answer timer starting
2. Click "Use voice input" checkbox
3. Click microphone button
4. Speak an answer (or type if voice isn't available)

**Sample Answer to Speak:**
"In my role at TechCorp, I led the migration from a monolithic architecture to microservices. The situation was that our system couldn't scale to handle growing user traffic. My task was to break down the monolith into manageable services.

I started by analyzing the codebase to identify service boundaries, then implemented services using Docker and Kubernetes. We used Node.js for some services and Python for others, depending on the use case.

As a result, we improved system scalability by 300%, reduced deployment times from 2 hours to 15 minutes, and achieved 99.9% uptime. The architecture now serves over 1 million users."

**Script:**
"Now I'm answering with voice input. The system uses the Web Speech API to transcribe my speech in real-time. You can see the transcript appearing as I speak.

I'm demonstrating the STAR method here - Situation, Task, Action, Result - which the system will detect and evaluate.

Notice the 3-minute timer - if you run over time, the system will automatically submit your answer. You can also click 'Submit Answer' to finish early."

**Actions:**
1. Click "Submit Answer"
2. Show loading state

---

### Part 5: Intelligent Follow-Up (4:30 - 5:30)

**[Screen: Follow-up question appears]**

**Script:**
"Here's where the 'Mahesh mindset' really shines. Based on my answer, the AI has generated an intelligent follow-up question. It detected that I mentioned scalability improvements and wants me to elaborate on specific technical details.

This is the adaptive intelligence - if I had given a weak or off-topic answer, it would have redirected me. If I seemed confused, it would provide hints. If I were overly verbose, it would gently refocus me.

Let me answer this follow-up quickly..."

**Actions:**
1. Type or speak a brief follow-up answer:
   "We used horizontal pod autoscaling in Kubernetes based on CPU and memory metrics. We also implemented Redis caching for frequently accessed data, which reduced database load by 40%."

2. Submit answer
3. Show next question appearing

---

### Part 6: Demonstrating Intelligent Behavior (5:30 - 6:30)

**[Screen: Second question]**

**Script:**
"Let me demonstrate another intelligent behavior. I'm going to give an intentionally off-topic answer to show how the system redirects..."

**Actions:**
1. Start answering the question about teamwork/conflict
2. Type an off-topic answer:
   "I really enjoy working with databases. SQL is my favorite because it's so powerful for querying data..."

3. Submit answer
4. Show the redirection follow-up

**Script:**
"See that? The system detected I drifted off-topic and politely redirected me back to the question about team conflict. This is persona detection in action - it recognized this as an 'off-track' response and adapted its approach.

This same system can detect:
- Confused users who need guidance
- Efficient users who should be challenged more
- Chatty users who need refocusing
- Edge cases like nonsense answers

Let me give a proper answer now..."

---

### Part 7: Completing Interview (6:30 - 7:00)

**[Screen: Skip through remaining questions quickly]**

**Script:**
"I'll quickly complete the remaining questions to generate the report. In a real interview, you'd answer all 5 questions thoroughly, but for demo purposes, I'll speed through these..."

**Actions:**
1. Answer remaining questions briefly (can fast-forward or show montage)
2. Click through to completion

---

### Part 8: Performance Report (7:00 - 9:00)

**[Screen: Report viewer]**

**Script:**
"And here's the comprehensive performance report! 

Look at this - the system has evaluated my entire interview across multiple dimensions:

**Overall Score: 78/100** - rated as 'Intermediate' candidate, ready for interviews.

The score breakdown shows:
- Confidence: 82/100 - Good assertiveness in answers
- Communication: 85/100 - Clear and structured
- Technical Depth: 75/100 - Solid understanding
- STAR Method: 70/100 - Mostly followed the structure
- Behavioral Clarity: 80/100 - Relevant examples

**Strengths identified:**
- Strong use of specific examples and metrics
- Good STAR method structure in most answers
- Clear communication style
- Technical knowledge demonstrated well

**Areas for improvement:**
- Could quantify more achievements
- Some answers could be more concise
- Practice explaining complex concepts more simply

**Improvement suggestions:**
- Practice STAR method consistently
- Prepare 10 key stories from your experience
- Record yourself answering questions
- Focus on quantifiable impacts

The system also detected my 'persona' throughout the interview - mostly 'efficient' with one 'off-track' moment when I gave that intentional wrong answer.

Now I can download this as a PDF report or JSON data for further analysis."

**Actions:**
1. Scroll through report sections
2. Click "Download PDF Report"
3. Show PDF opening
4. Click "Download JSON Data"
5. Show JSON file

---

### Part 9: Code Architecture Walkthrough (9:00 - 10:00)

**[Screen: VS Code with project structure]**

**Script:**
"Let me quickly show you the architecture behind this.

The backend is built with FastAPI and uses a modular agent-based architecture:

- **ResumeParser**: LLM-powered extraction of structured data
- **QuestionGenerator**: Creates personalized questions
- **PersonaDetector**: Identifies user behavior patterns
- **ResponseEvaluator**: Scores answers across multiple dimensions
- **FollowUpEngine**: Generates intelligent follow-ups
- **STARChecker**: Detects STAR method usage
- **ReportGenerator**: Creates comprehensive reports

The frontend is React with:
- Real-time voice recording using Web Speech API
- Dual countdown timers (30-sec prep, 3-min answer)
- Clean, responsive UI
- PDF and JSON export

Everything is containerized with Docker, tested with pytest, and ready to deploy to Render, Railway, Vercel, or any cloud platform.

The system uses GPT-4 by default but can switch to Anthropic Claude or local models. It includes mock responses for testing without API keys."

**Actions:**
1. Show backend folder structure
2. Show agent modules
3. Show frontend components
4. Show Docker files
5. Show test files

---

### Part 10: Conclusion (10:00)

**[Screen: Back to homepage or README]**

**Script:**
"That's the Interview Practice Partner - a complete, production-ready AI interview system built with intelligence, adaptability, and clean architecture.

Every edge case is handled:
- ✅ Off-topic answers → redirected
- ✅ Confused users → guided
- ✅ Time management → enforced
- ✅ Voice and text input → supported
- ✅ Comprehensive reports → generated

This project is fully documented, tested, and ready for deployment. Check out the GitHub repository for setup instructions.

Thank you for watching!"

---

## Post-Recording Checklist

- [ ] Trim any dead air
- [ ] Add title slide at beginning
- [ ] Add subtitle captions if needed
- [ ] Add background music (optional, keep low)
- [ ] Export at 1080p, 30fps
- [ ] Upload to YouTube/Vimeo
- [ ] Add to GitHub README
- [ ] Share on LinkedIn/Twitter

---

## Quick Tips for Recording

1. **Speak clearly and at moderate pace**
2. **Pause between sections** (easier to edit)
3. **Show, don't just tell** - demonstrate features
4. **Keep energy high** but natural
5. **Practice the demo** before recording
6. **Have backup plan** if voice recording fails
7. **Highlight unique features** (persona detection, timers, intelligent follow-ups)
8. **End with clear call-to-action**

---

## Alternative: 5-Minute Quick Demo

If you need a shorter version, focus on:
1. Introduction (30 sec)
2. Resume upload (30 sec)
3. One complete question cycle (2 min)
4. Intelligent follow-up demo (1 min)
5. Report showcase (1 min)

---

## Thumbnail Ideas

- Split screen: User speaking + AI analyzing
- "78/100" score with checkmark
- "AI Interview Coach" with robot icon
- Before/After interview preparation comparison
