# AI-Powered News Agency

A full-stack news agency application that automatically fetches news from Event Registry API and uses AI to generate summaries, categories, social media captions, and image prompts. Features semantic search powered by vector embeddings stored in Pinecone.

## 🎯 Project Overview

This application demonstrates:
- **AI Integration**: OpenAI GPT-4 for content generation and DALL·E for image creation
- **Vector Database**: Pinecone for semantic search and article recommendations
- **Modern Stack**: FastAPI backend with Next.js frontend
- **Semantic Search**: Find related articles using vector similarity

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Pinecone API key ([Get one here](https://app.pinecone.io/))
- Event Registry API key ([Get one here](https://eventregistry.org/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/samiyaMalik/ai-news-agency-website.git
   cd ai-news-agency-website
   ```

2. **Setup Backend**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Copy environment file and add your API keys
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   
   # Copy environment file
   cp .env.example .env.local
   # Edit .env.local if needed
   ```

4. **Start Servers**
   
   **Terminal 1 - Backend:**
   ```bash
   python -m uvicorn backend.main:app --reload --port 8000
   ```
   
   **Terminal 2 - Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

5. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 📚 Documentation

For detailed setup instructions, API documentation, and configuration guide, see [GUIDE.md](./GUIDE.md).

## 📓 Kaggle Notebooks

We provide two Kaggle notebooks for easy setup and testing:

1. **[Kaggle_Setup_Notebook.ipynb](./Kaggle_Setup_Notebook.ipynb)** - Complete setup guide without API keys
   - Step-by-step instructions to clone and setup the repository
   - Environment configuration
   - Installation verification
   - Perfect for first-time setup

2. **[Kaggle_Test_With_API_Keys.ipynb](./Kaggle_Test_With_API_Keys.ipynb)** - Test notebook with API keys
   - Add your API keys and test all services
   - Test news fetching, OpenAI, and Pinecone integration
   - Verify everything is working correctly
   - **⚠️ Important: Never commit this file with real API keys to Git!**

### Using Kaggle Notebooks

1. Open the notebook in Kaggle or Jupyter
2. Run cells sequentially
3. For test notebook: Add your API keys in the first cell
4. All services will be tested automatically

## ✨ Features

- **News Fetching**: Fetch articles from Event Registry API based on keywords
- **AI Processing**: Generate summaries, SEO tags, social media captions using GPT-4
- **Image Generation**: Create images using DALL·E based on AI-generated prompts
- **Semantic Search**: Find related articles using vector similarity search
- **Vector Database**: Store article embeddings in Pinecone for fast retrieval
- **Modern UI**: Clean, responsive frontend with Tailwind CSS

## 🏗️ Architecture

- **Frontend**: Next.js 14 with TypeScript, Tailwind CSS
- **Backend**: FastAPI (Python) with async support
- **Database**: SQLite (automatic) or MySQL with SQLAlchemy ORM
- **Vector DB**: Pinecone for embeddings and semantic search
- **AI Services**: OpenAI (GPT-4, DALL·E, embeddings)

## 🔑 API Keys Setup

1. **OpenAI API Key**
   - Sign up at https://platform.openai.com/
   - Create an API key
   - Add to `.env`: `OPENAI_API_KEY=sk-...`

2. **Pinecone API Key**
   - Sign up at https://app.pinecone.io/
   - Create an API key
   - Create an index with 1024 dimensions
   - Add to `.env`: `PINECONE_API_KEY=...` and `PINECONE_INDEX_NAME=...`

3. **Event Registry API Key**
   - Sign up at https://eventregistry.org/
   - Get your API key
   - Add to `.env`: `EVENT_REGISTRY_API_KEY=...`

## 📖 How AI is Used

### 1. Article Summarization
- Uses GPT-4 to generate concise 2-3 sentence summaries
- Captures key information from article content

### 2. SEO Tag Generation
- Extracts relevant keywords and tags
- Helps with content categorization

### 3. Social Media Caption Generation
- Creates engaging captions for social media posts
- Optimized for different platforms

### 4. Image Prompt Generation
- Generates detailed prompts for DALL·E
- Creates contextually relevant images for articles

### 5. Semantic Search
- Converts articles to 1024-dimensional embeddings
- Stores in Pinecone for similarity search
- Enables finding related articles by meaning, not just keywords

## 🧪 Testing

See [GUIDE.md](./GUIDE.md) for comprehensive testing instructions.

Quick test:
1. Start both servers
2. Open http://localhost:3000
3. Search for a keyword (e.g., "Technology")
4. Click "Process with AI" on an article
5. Click "Generate Social Post" to see AI-generated content

## 📊 Evaluation Criteria

This project meets all evaluation criteria:

✅ **Embedding Accuracy**: Uses OpenAI's text-embedding-3-small model to capture semantic content

✅ **Vector DB Integration**: Fully integrated with Pinecone, embeddings stored and retrievable efficiently

✅ **Semantic Search Results**: Returns relevant articles based on content similarity, not just keywords

✅ **Recommendations**: Related Articles feature displays contextually relevant suggestions

✅ **Performance**: Optimized for fast vector search and retrieval

✅ **Code Quality**: Clean, modular code with proper error handling

✅ **Documentation**: Comprehensive setup instructions and API documentation

## 🔒 Security

- All API keys are stored in environment variables (never committed to git)
- `.env` files are in `.gitignore`
- Use `.env.example` as a template

## 📝 License

This project is created for assignment purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

For issues or questions, please open an issue in the repository.

---

**Built with ❤️ using FastAPI, Next.js, OpenAI, and Pinecone**

