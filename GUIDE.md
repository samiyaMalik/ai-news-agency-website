# AI-Powered News Agency - Complete Setup & Usage Guide

A comprehensive guide for setting up, configuring, and using the AI-Powered News Agency application.

---

## 📋 Table of Contents

1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Getting API Keys](#getting-api-keys)
4. [Installation Guide](#installation-guide)
5. [Configuration](#configuration)
6. [Running the Application](#running-the-application)
7. [Using the Application](#using-the-application)
8. [API Documentation](#api-documentation)
9. [Troubleshooting](#troubleshooting)
10. [Advanced Configuration](#advanced-configuration)
11. [Deployment](#deployment)

---

## 🎯 Introduction

This application is a full-stack news agency platform that:
- Fetches news articles from Event Registry API
- Uses AI (OpenAI GPT-4) to generate summaries, tags, and captions
- Creates images using DALL·E
- Provides semantic search using Pinecone vector database
- Offers a modern web interface built with Next.js

---

## 💻 System Requirements

### Minimum Requirements

- **Operating System:** Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python:** 3.9 or higher
- **Node.js:** 18.0 or higher
- **RAM:** 4GB minimum (8GB recommended)
- **Disk Space:** 500MB free space
- **Internet Connection:** Required for API calls

### Software Installation

1. **Python Installation:**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"
   - Verify: `python --version` (should show 3.9+)

2. **Node.js Installation:**
   - Download from: https://nodejs.org/
   - Install LTS version (recommended)
   - Verify: `node --version` (should show 18+)
   - Verify: `npm --version` (should be included)

3. **Git Installation:**
   - Download from: https://git-scm.com/downloads
   - Verify: `git --version`

---

## 🔑 Getting API Keys

### 1. OpenAI API Key

1. Visit: https://platform.openai.com/
2. Sign up or log in
3. Go to: API Keys section
4. Click: "Create new secret key"
5. Copy the key (starts with `sk-`)
6. **Important:** Save it securely - you won't see it again

**Pricing:** Pay-as-you-go. Check current pricing on OpenAI website.

### 2. Pinecone API Key

1. Visit: https://app.pinecone.io/
2. Sign up for free account
3. Go to: API Keys section
4. Copy your API key
5. **Create an Index:**
   - Click "Create Index"
   - Name: Choose any name (e.g., `ai-news-index`)
   - Dimensions: **1024** (important!)
   - Metric: Cosine similarity
   - Cloud: AWS (or your preference)
   - Region: us-east-1 (or your preference)
   - Type: Dense
   - Capacity Mode: Serverless (recommended for free tier)
6. Copy the index name

**Free Tier:** Available with limitations. Check Pinecone website for details.

### 3. Event Registry API Key

1. Visit: https://eventregistry.org/
2. Sign up for free account
3. Go to: API section
4. Generate API key
5. Copy the key

**Free Tier:** Limited requests per day. Check Event Registry website for limits.

---

## 📥 Installation Guide

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/samiyaMalik/ai-news-agency-website.git

# Navigate to project directory
cd ai-news-agency-website
```

### Step 2: Backend Installation

#### 2.1 Install Python Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

**Troubleshooting:**
- If `pip` doesn't work, try `pip3`
- On Linux/Mac, you might need `sudo pip install -r requirements.txt`
- For permission issues: `pip install --user -r requirements.txt`
- For virtual environment (recommended):
  ```bash
  python -m venv venv
  # Windows:
  venv\Scripts\activate
  # Mac/Linux:
  source venv/bin/activate
  pip install -r requirements.txt
  ```

#### 2.2 Verify Installation

```bash
# Check if FastAPI is installed
python -c "import fastapi; print('FastAPI installed successfully')"
```

### Step 3: Frontend Installation

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install
```

**Troubleshooting:**
- If `npm install` fails, try deleting `node_modules` and `package-lock.json`, then run again
- On some systems: `npm install --legacy-peer-deps`
- Clear npm cache: `npm cache clean --force`

---

## ⚙️ Configuration

### Backend Configuration

1. **Copy environment template:**
   ```bash
   # From project root
   cp .env.example .env
   ```
   
   **Windows:**
   ```bash
   copy .env.example .env
   ```

2. **Edit `.env` file:**
   Open `.env` in any text editor and replace placeholders:

   ```env
   # OpenAI Configuration (Required)
   OPENAI_API_KEY=sk-your-actual-openai-key-here
   
   # Pinecone Configuration (Required)
   PINECONE_API_KEY=your-actual-pinecone-key-here
   PINECONE_ENVIRONMENT=us-east-1
   PINECONE_INDEX_NAME=your-actual-index-name-here
   
   # Event Registry API (Required)
   EVENT_REGISTRY_API_KEY=your-actual-event-registry-key-here
   
   # Frontend Configuration
   FRONTEND_URL=http://localhost:3000
   
   # Server Configuration
   BACKEND_PORT=8000
   ```

3. **Save the file**

### Frontend Configuration (Optional)

The frontend works with defaults, but you can customize:

1. **Copy environment template:**
   ```bash
   cd frontend
   cp .env.example .env.local
   ```

2. **Edit `.env.local` if needed:**
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```

---

## 🚀 Running the Application

### Method 1: Manual (Two Terminals)

#### Terminal 1 - Backend Server

```bash
# From project root directory
python -m uvicorn backend.main:app --reload --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**✅ Success Indicators:**
- "Application startup complete" message
- No error messages
- Server listening on port 8000

#### Terminal 2 - Frontend Server

```bash
# Navigate to frontend directory
cd frontend

# Start development server
npm run dev
```

**Expected Output:**
```
> ai-news-agency-website@0.1.0 dev
> next dev

  ▲ Next.js 14.x.x
  - Local:        http://localhost:3000
  - ready started server on 0.0.0.0:3000
```

**✅ Success Indicators:**
- "ready started server" message
- No error messages
- Server listening on port 3000

### Method 2: Using Batch Scripts (Windows)

If `START_SERVERS.bat` exists:

```bash
START_SERVERS.bat
```

This will start both servers automatically.

---

## 🎮 Using the Application

### Accessing the Application

1. **Open your web browser**
2. **Navigate to:** http://localhost:3000
3. **You should see:** AI News Agency homepage with search box

### Basic Workflow

#### 1. Search for News

1. Enter a keyword in the search box (e.g., "Technology", "India", "Sports")
2. Click "Search News" button
3. Wait 10-30 seconds for articles to load
4. Articles will appear with:
   - Title
   - Image (if available)
   - Published date
   - Source name
   - Preview content

#### 2. Process Article with AI

1. Click "Process with AI" button on any article
2. Wait 15-30 seconds (AI processing takes time)
3. You'll see:
   - ✅ Success message
   - AI-generated summary
   - SEO tags
   - Article is now stored in database

#### 3. Generate Social Media Post

1. Click "Generate Social Post" button on a processed article
2. Wait 10-20 seconds
3. A modal will open showing:
   - AI-generated caption
   - DALL·E generated image
   - Ready to share on social media

#### 4. View Article Details

1. Click on any article title
2. View full article details
3. See related articles (if available)
4. View AI-generated content

### Advanced Features

#### Semantic Search

1. Use the API documentation: http://localhost:8000/docs
2. Try the `/api/articles/semantic-search` endpoint
3. Enter a query (e.g., "technology innovation")
4. Get semantically similar articles

#### Related Articles

- Process multiple articles with AI
- Click on an article to view details
- Scroll to "Related Articles" section
- See articles similar in meaning (not just keywords)

---

## 📚 API Documentation

### Interactive API Docs

Visit: http://localhost:8000/docs

This provides:
- Swagger UI interface
- All available endpoints
- Try out endpoints directly
- See request/response formats

### Key Endpoints

#### 1. Fetch News Articles

```http
POST /api/news/fetch
Content-Type: application/json

{
  "keyword": "Technology",
  "articles_count": 100,
  "articles_page": 1
}
```

**Response:**
```json
{
  "articles": [...],
  "total_fetched": 50,
  "keyword": "Technology"
}
```

#### 2. Get All Articles

```http
GET /api/articles?page=1&page_size=20
```

#### 3. Process Article with AI

```http
POST /api/articles/{id}/process-ai
```

This generates:
- AI summary
- SEO tags
- Social media caption
- Image prompt
- Vector embedding (stored in Pinecone)

#### 4. Semantic Search

```http
POST /api/articles/semantic-search
Content-Type: application/json

{
  "query": "technology innovation",
  "top_k": 10
}
```

#### 5. Get Related Articles

```http
GET /api/articles/{id}/related?top_k=5
```

#### 6. Get Social Media Post

```http
GET /api/articles/{id}/social-post
```

Returns caption and DALL·E image.

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### Backend Won't Start

**Problem:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
pip install -r requirements.txt
```

**Problem:** Port 8000 already in use

**Solution:**
- Change port in `.env`: `BACKEND_PORT=8001`
- Or stop the process using port 8000:
  ```bash
  # Windows
  netstat -ano | findstr :8000
  taskkill /PID <PID> /F
  
  # Mac/Linux
  lsof -ti:8000 | xargs kill
  ```

#### Frontend Won't Start

**Problem:** Port 3000 already in use

**Solution:**
- Kill the process:
  ```bash
  # Windows
  netstat -ano | findstr :3000
  taskkill /PID <PID> /F
  
  # Mac/Linux
  lsof -ti:3000 | xargs kill
  ```

**Problem:** `npm install` fails

**Solution:**
```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

#### API Keys Not Working

**Problem:** "Invalid API key" errors

**Solution:**
1. Verify keys in `.env` file
2. Check for extra spaces or quotes
3. Ensure keys are on single line
4. Restart backend server after changing `.env`

#### Database Issues

**Problem:** SQLite errors

**Solution:**
- SQLite works automatically
- If issues, delete `ai_news_agency.db` and restart
- Database will be recreated automatically

**Problem:** MySQL connection errors

**Solution:**
1. Verify MySQL is running
2. Check credentials in `.env`
3. Ensure database exists:
   ```sql
   CREATE DATABASE ai_news_agency CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

#### Pinecone Issues

**Problem:** "Index not found"

**Solution:**
1. Verify index name in `.env` matches Pinecone dashboard
2. Check index dimensions are 1024
3. Ensure index is in the correct region

**Problem:** "Invalid API key"

**Solution:**
1. Verify Pinecone API key in `.env`
2. Check PINECONE_ENVIRONMENT matches your index region
3. Verify key is active in Pinecone dashboard

#### OpenAI Issues

**Problem:** "Insufficient quota"

**Solution:**
1. Check OpenAI account balance
2. Verify API key has credits
3. Check usage limits in OpenAI dashboard

**Problem:** "Model not found"

**Solution:**
1. Ensure GPT-4 access is enabled in your OpenAI account
2. Check account tier/limits
3. Verify API key permissions

#### Frontend Not Connecting to Backend

**Problem:** CORS errors or connection refused

**Solution:**
1. Verify backend is running on port 8000
2. Check `NEXT_PUBLIC_API_URL` in `frontend/.env.local`
3. Ensure backend CORS allows `http://localhost:3000`
4. Check browser console (F12) for errors

---

## 🔧 Advanced Configuration

### Using MySQL Database

1. **Install MySQL:**
   - Download from: https://dev.mysql.com/downloads/mysql/

2. **Create Database:**
   ```sql
   CREATE DATABASE ai_news_agency CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. **Update `.env`:**
   ```env
   DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/ai_news_agency
   ```

4. **Run Migrations:**
   ```bash
   cd backend
   alembic upgrade head
   ```

### Custom Ports

**Backend:**
```env
BACKEND_PORT=8001
```

**Frontend:**
Edit `frontend/package.json`:
```json
"scripts": {
  "dev": "next dev -p 3001"
}
```

### Environment-Specific Configuration

Create different `.env` files:
- `.env.development` - Development settings
- `.env.production` - Production settings

Load specific file:
```bash
# Linux/Mac
export ENV_FILE=.env.production

# Windows
set ENV_FILE=.env.production
```

---

## 🚀 Deployment

### Backend Deployment

#### Option 1: Railway

1. Sign up at https://railway.app/
2. Create new project
3. Connect GitHub repository
4. Add environment variables
5. Deploy automatically

#### Option 2: Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Set environment variables:
   ```bash
   heroku config:set OPENAI_API_KEY=your-key
   heroku config:set PINECONE_API_KEY=your-key
   # ... etc
   ```
5. Deploy: `git push heroku main`

#### Option 3: DigitalOcean

1. Create Droplet
2. Install Python and dependencies
3. Use systemd to run uvicorn
4. Configure nginx as reverse proxy

### Frontend Deployment

#### Option 1: Vercel (Recommended)

1. Sign up at https://vercel.com/
2. Import GitHub repository
3. Set environment variable: `NEXT_PUBLIC_API_URL`
4. Deploy automatically

#### Option 2: Netlify

1. Sign up at https://netlify.com/
2. Connect repository
3. Build command: `cd frontend && npm run build`
4. Publish directory: `frontend/out`
5. Set environment variables

#### Option 3: Self-Hosted

1. Build production bundle:
   ```bash
   cd frontend
   npm run build
   ```
2. Serve with nginx or Apache
3. Configure reverse proxy to backend

---

## 📊 Performance Tips

1. **Database Indexing:** Already configured for optimal performance
2. **Caching:** Consider Redis for production
3. **CDN:** Use CDN for static assets
4. **Rate Limiting:** Implement rate limiting for APIs
5. **Monitoring:** Set up monitoring (e.g., Sentry)

---

## 🔒 Security Best Practices

1. **Never commit `.env` files** - Already in `.gitignore`
2. **Use environment variables** - Never hardcode keys
3. **Rotate API keys regularly**
4. **Use HTTPS in production**
5. **Implement authentication** for production use
6. **Set up CORS properly** for production domains

---

## 📞 Support

### Getting Help

1. **Check this guide** - Most issues are covered here
2. **Check README.md** - Quick reference
3. **API Documentation** - http://localhost:8000/docs
4. **GitHub Issues** - Open an issue on the repository

### Reporting Issues

When reporting issues, include:
- Operating system and version
- Python version: `python --version`
- Node.js version: `node --version`
- Error messages (full traceback)
- Steps to reproduce
- What you've tried

---

## 🎓 Learning Resources

- **FastAPI:** https://fastapi.tiangolo.com/
- **Next.js:** https://nextjs.org/docs
- **OpenAI API:** https://platform.openai.com/docs
- **Pinecone:** https://docs.pinecone.io/
- **Event Registry:** https://eventregistry.org/documentation

---

## 📝 License

This project is created for assignment purposes.

---

## 🙏 Acknowledgments

Built with:
- FastAPI - Modern Python web framework
- Next.js - React framework for production
- OpenAI - AI models and embeddings
- Pinecone - Vector database
- Event Registry - News data API

---

**Last Updated:** Complete guide with all setup, configuration, usage, and deployment instructions.

**Version:** 1.0.0

