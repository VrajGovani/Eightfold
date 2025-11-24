# Deployment Guide

## Quick Start (Local Development)

### Prerequisites
```bash
# Install Python 3.9+
python --version

# Install Node.js 18+
node --version

# Install pip and npm
pip --version
npm --version
```

### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy ..\.env.example .env
# Edit .env with your OpenAI API key

# Run backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Create .env file
copy .env.example .env

# Run frontend
npm start
```

Frontend available at: http://localhost:3000

---

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Make sure Docker and Docker Compose are installed
docker --version
docker-compose --version

# Set environment variables
copy .env.example .env
# Edit .env with your API keys

# Build and run
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

### Individual Docker Containers

```bash
# Build backend
docker build -f Dockerfile.backend -t interview-backend .

# Run backend
docker run -p 8000:8000 --env-file .env interview-backend

# Build frontend
docker build -f Dockerfile.frontend -t interview-frontend .

# Run frontend
docker run -p 3000:3000 interview-frontend
```

---

## Cloud Deployment

### Deploy to Render

#### Backend (Web Service)

1. Create new Web Service on Render
2. Connect your GitHub repository
3. Configure:
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment:** Python 3.11
4. Add environment variables:
   ```
   OPENAI_API_KEY=your-key
   LLM_PROVIDER=openai
   LLM_MODEL=gpt-4-turbo-preview
   ALLOWED_ORIGINS=https://your-frontend.onrender.com
   ```
5. Deploy

#### Frontend (Static Site)

1. Create new Static Site on Render
2. Connect your GitHub repository
3. Configure:
   - **Build Command:** `cd frontend && npm install && npm run build`
   - **Publish Directory:** `frontend/build`
4. Add environment variable:
   ```
   REACT_APP_API_URL=https://your-backend.onrender.com
   ```
5. Deploy

### Deploy to Railway

#### One-Click Deploy

1. Click "Deploy on Railway" button (add to README)
2. Configure environment variables
3. Railway will auto-detect and deploy both services

#### Manual Deploy

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize
railway init

# Deploy backend
cd backend
railway up

# Deploy frontend
cd ../frontend
railway up

# Set environment variables
railway variables set OPENAI_API_KEY=your-key
```

### Deploy to Vercel + Render

#### Frontend on Vercel

```bash
# Install Vercel CLI
npm install -g vercel

cd frontend

# Deploy
vercel --prod

# Set environment variables in Vercel dashboard
REACT_APP_API_URL=https://your-backend.onrender.com
```

#### Backend on Render
Follow Render backend instructions above.

### Deploy to AWS

#### Using EC2

1. Launch EC2 instance (Ubuntu 22.04)
2. SSH into instance
3. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3-pip nodejs npm nginx
   ```
4. Clone repository
5. Setup backend as systemd service
6. Configure Nginx as reverse proxy
7. Setup SSL with Let's Encrypt

#### Using ECS (Docker)

1. Build and push Docker images to ECR
2. Create ECS cluster
3. Define task definitions
4. Create services
5. Configure ALB

### Deploy to Azure

#### Using Azure Container Instances

```bash
# Login
az login

# Create resource group
az group create --name interview-rg --location eastus

# Deploy containers
az container create \
  --resource-group interview-rg \
  --name interview-backend \
  --image your-registry/interview-backend \
  --dns-name-label interview-backend \
  --ports 8000

az container create \
  --resource-group interview-rg \
  --name interview-frontend \
  --image your-registry/interview-frontend \
  --dns-name-label interview-frontend \
  --ports 3000
```

### Deploy to GCP

#### Using Cloud Run

```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT-ID/interview-backend backend/
gcloud builds submit --tag gcr.io/PROJECT-ID/interview-frontend frontend/

# Deploy backend
gcloud run deploy interview-backend \
  --image gcr.io/PROJECT-ID/interview-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Deploy frontend
gcloud run deploy interview-frontend \
  --image gcr.io/PROJECT-ID/interview-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## Environment Variables

### Backend (.env)
```bash
# Required
OPENAI_API_KEY=sk-...
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo-preview

# Optional
ANTHROPIC_API_KEY=sk-ant-...
MAX_TOKENS=2000
TEMPERATURE=0.7
ALLOWED_ORIGINS=http://localhost:3000,https://your-domain.com
LOG_LEVEL=INFO
DATABASE_URL=sqlite:///./interview_practice.db
SECRET_KEY=your-secret-key
```

### Frontend (.env)
```bash
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws
REACT_APP_ENV=production
```

---

## Production Checklist

- [ ] Set strong SECRET_KEY
- [ ] Configure proper CORS origins
- [ ] Enable HTTPS/SSL
- [ ] Set up database (PostgreSQL recommended)
- [ ] Configure proper logging
- [ ] Set up monitoring (Sentry, DataDog, etc.)
- [ ] Enable rate limiting
- [ ] Configure CDN for frontend
- [ ] Set up backup strategy
- [ ] Configure auto-scaling
- [ ] Set up CI/CD pipeline
- [ ] Enable error tracking
- [ ] Configure health checks
- [ ] Set up load balancer

---

## Monitoring & Logging

### Add Sentry (Error Tracking)

Backend:
```python
import sentry_sdk
sentry_sdk.init(dsn="your-dsn")
```

Frontend:
```javascript
import * as Sentry from "@sentry/react";
Sentry.init({ dsn: "your-dsn" });
```

### Logs

Backend logs available at:
- Docker: `docker-compose logs backend`
- Production: Check cloud provider logs

Frontend logs available in browser console.

---

## Scaling Considerations

### Horizontal Scaling
- Use load balancer (Nginx, AWS ALB, etc.)
- Deploy multiple backend instances
- Use session storage (Redis, database)

### Database
- Switch from SQLite to PostgreSQL
- Use connection pooling
- Enable database replication

### Caching
- Add Redis for session management
- Cache LLM responses for common patterns
- Use CDN for frontend assets

---

## Security Best Practices

1. **API Keys:** Never commit to git, use environment variables
2. **CORS:** Restrict to specific domains in production
3. **Rate Limiting:** Implement on API endpoints
4. **Input Validation:** Already implemented in validators
5. **HTTPS:** Always use SSL certificates in production
6. **Authentication:** Add if needed (JWT, OAuth)
7. **File Upload:** Validate file types and sizes (implemented)

---

## Troubleshooting

### Backend won't start
- Check Python version (3.9+)
- Verify all dependencies installed
- Check .env file exists and has valid API key
- Check port 8000 is not in use

### Frontend won't connect to backend
- Verify REACT_APP_API_URL is correct
- Check CORS settings in backend
- Verify backend is running

### LLM API errors
- Check API key is valid
- Verify account has credits
- Check rate limits

### Docker issues
- Ensure Docker daemon is running
- Check port conflicts
- Verify .env file is present

---

## Performance Optimization

1. **Backend:**
   - Use async/await for all I/O operations
   - Implement response caching
   - Use connection pooling
   - Optimize LLM prompts

2. **Frontend:**
   - Code splitting
   - Lazy loading
   - Compress images
   - Use production build

---

## Backup & Recovery

### Database Backup
```bash
# SQLite
cp interview_practice.db interview_practice_backup.db

# PostgreSQL
pg_dump dbname > backup.sql
```

### Session Data
- Store session data in persistent storage
- Implement periodic backups
- Keep backup retention policy

---

For more details, see the main README.md file.
