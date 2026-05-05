# AEO Diagnostic Tool 🔍

<p align="center">
  <strong>Discover how AI assistants recommend your product — and beat your competition.</strong>
</p>

<p align="center">
  <a href="https://aeo-checker-fds07ppu3-sarthaksenapatis-projects.vercel.app/">🌐 Live Frontend (Vercel)</a> •
  <a href="https://aeo-diagnostic.onrender.com/">⚡ Live Backend (Render)</a> •
  <a href="https://github.com/sarthaksenapati/aeo-diagnostic/issues">🐛 Report Bug</a> •
  <a href="https://github.com/sarthaksenapati/aeo-diagnostic/issues">✨ Request Feature</a>
</p>

---

## 📖 What is AEO?

**Answer Engine Optimization (AEO)** is the practice of optimizing your product or brand to appear in AI-generated answers. As more users turn to AI assistants like ChatGPT, Gemini, and Perplexity for product recommendations, traditional SEO is no longer enough.

AEO Diagnostic helps you understand:
- ✅ Is your product mentioned by AI models?
- 📊 How prominently is it recommended?
- 😊 What sentiment do AI models express about it?
- 🥊 How do you compare to your competitors?

---

## 🚀 Live Demo

| Component | URL | Platform |
|-----------|-----|----------|
| **Next.js Frontend** | [https://aeo-checker-fds07ppu3-sarthaksenapatis-projects.vercel.app/](https://aeo-checker-fds07ppu3-sarthaksenapatis-projects.vercel.app/) | Vercel |
| **FastAPI Backend** | [https://aeo-diagnostic.onrender.com/](https://aeo-diagnostic.onrender.com/) | Render |

---

## ✨ Features

### 🎯 Core Analysis
- **Multi-Model Querying**: Simultaneously queries 3 leading AI models:
  - 🟢 **Gemma 3 27B** (Google)
  - 🔵 **Nemotron 3 Super 120B** (NVIDIA via OpenRouter)
  - 🟣 **GPT OSS 120B** (OpenAI via OpenRouter)

### 📊 Detailed Metrics
- **Mention Detection**: Checks if your product appears in AI responses using advanced variant matching
- **Position Analysis**: Determines if your product appears in the top, middle, or late section of responses
- **Sentiment Analysis**: Analyzes the context around your product mention (Positive, Negative, Neutral)
- **AEO Scoring**: Proprietary scoring system (0-10) based on mention position and sentiment

### 🥊 Competitor Comparison
- Side-by-side comparison with competitors
- Visual charts showing your score vs. competitor scores across all models
- Actionable insights on who's winning and why

### 💡 AI-Powered Recommendations
- Personalized recommendations based on your AEO score
- Competitor-specific strategies
- Actionable tips to improve AI visibility

### 🎨 Modern UI
- **Next.js Frontend**: Beautiful, dark-themed UI with:
  - Interactive gauge charts
  - Model comparison cards
  - Real-time analysis visualization
  - Responsive design
- **Streamlit Frontend**: Alternative lightweight interface for quick testing

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
├──────────────────────────┬──────────────────────────────────┤
│    Next.js Frontend      │     Streamlit Frontend           │
│    (Vercel Deployed)     │     (Local/Streamlit Cloud)      │
└────────────┬─────────────┴──────────────┬───────────────────┘
             │                            │
             └────────────┬───────────────┘
                          │ HTTP Requests
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend (Render)                   │
│  - /analyze endpoint                                        │
│  - Async parallel LLM queries                               │
│  - Ranking analysis                                         │
│  - Sentiment analysis                                       │
│  - Recommendation engine                                    │
└────────────┬────────────────────────────────────────────────┘
             │
             ├─────────────────┬─────────────────┬─────────────────┐
             ▼                 ▼                 ▼                 ▼
      ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
      │   Gemini    │   │ OpenRouter  │   │ OpenRouter  │   │  Analysis   │
      │   API       │   │ (Nemotron)  │   │  (GPT OSS)  │   │  Engine     │
      └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘
```

---

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **httpx**: Asynchronous HTTP client for parallel API calls
- **asyncio**: Concurrent LLM querying
- **Python-dotenv**: Environment variable management

### Frontend (Next.js)
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **shadcn/ui**: Beautiful, accessible UI components
- **Plotly.js**: Interactive charts and visualizations
- **Vercel**: Deployment platform

### Frontend (Streamlit - Alternative)
- **Streamlit**: Rapid UI development
- **Plotly**: Data visualization
- **Streamlit Components**: HTML/JS rendering

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 18+ (for Next.js frontend)
- API Keys:
  - [Gemini API Key](https://ai.google.dev/)
  - [OpenRouter API Key](https://openrouter.ai/)

### 1. Clone the Repository
```bash
git clone https://github.com/sarthaksenapati/aeo-diagnostic.git
cd aeo-diagnostic
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 4. Run Backend Locally
```bash
uvicorn main:app --reload
```
Backend will be available at `http://127.0.0.1:8000`

### 5. Frontend Setup (Next.js)
```bash
cd frontend
npm install  # or pnpm install
```

### 6. Run Frontend Locally
```bash
npm run dev
```
Frontend will be available at `http://localhost:3000`

### 7. Alternative: Streamlit Frontend
```bash
streamlit run frontend.py
```

---

## 📡 API Documentation

### Base URL
- Local: `http://127.0.0.1:8000`
- Production: `https://aeo-diagnostic.onrender.com`

### Endpoints

#### `POST /analyze`
Analyzes how AI models recommend a product.

**Request Body:**
```json
{
  "query": "best niacinamide serum for oily skin",
  "product": "Minimalist",
  "competitor": "The Ordinary"
}
```

**Response:**
```json
{
  "query": "best niacinamide serum for oily skin",
  "product": "Minimalist",
  "competitor": "The Ordinary",
  "results": {
    "Gemma 3 27B": {
      "response": "For oily skin, I recommend...",
      "analysis": {
        "mentioned": true,
        "rank": "Top mention",
        "score": 10,
        "sentiment": "Positive",
        "sentiment_emoji": "😊"
      },
      "competitor_analysis": {
        "mentioned": true,
        "rank": "Middle mention",
        "score": 6,
        "sentiment": "Positive",
        "sentiment_emoji": "😊"
      }
    }
  },
  "avg_score": 8.5,
  "recommendations": [
    "Your product has good AI visibility..."
  ]
}
```

---

## 📂 Project Structure

```
aeo-diagnostic/
├── main.py                 # FastAPI backend
├── frontend.py             # Streamlit frontend
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not tracked)
├── .gitignore
│
├── frontend/               # Next.js frontend
│   ├── app/
│   │   ├── page.tsx        # Main page
│   │   ├── layout.tsx      # Root layout
│   │   └── globals.css     # Global styles
│   ├── components/
│   │   ├── aeo/            # AEO-specific components
│   │   │   ├── gauge-chart.tsx
│   │   │   ├── model-card.tsx
│   │   │   ├── comparison-chart.tsx
│   │   │   └── ...
│   │   └── ui/             # shadcn/ui components
│   ├── lib/                # Utilities and types
│   ├── public/             # Static assets
│   ├── package.json
│   └── next.config.mjs
│
├── Procfile                # Render deployment config
├── render.yaml             # Render service definition
└── README.md
```

---

## 🧠 How It Works

### 1. Query Processing
When a user submits a query, the tool wraps it in a realistic prompt that mimics how customers actually ask AI assistants for recommendations.

### 2. Parallel LLM Queries
The backend simultaneously queries 3 AI models using async HTTP requests:
- **Gemini**: Direct API call to Google's Generative AI
- **Nemotron & GPT OSS**: Via OpenRouter API

### 3. Advanced Mention Detection
The analysis engine uses smart variant matching to detect product mentions:
- Handles "&" vs "and" variations
- Matches spaced and non-spaced versions
- Accounts for hyphenated variations

### 4. Position & Sentiment Analysis
- **Position**: Finds where the product is mentioned in the response
  - Top 30% = "Top mention" (Score: 10)
  - Middle 30-60% = "Middle mention" (Score: 6)
  - Bottom 40% = "Late mention" (Score: 3)
  - Not mentioned = Score: 0

- **Sentiment**: Analyzes 200 characters around the mention
  - Counts positive and negative keywords
  - Adjusts score based on sentiment

### 5. Recommendation Engine
Generates personalized recommendations based on:
- Overall AEO score
- Competitor comparison
- Industry best practices

---

## 🚀 Deployment

### Backend (Render)
The FastAPI backend is deployed on Render using:
- `render.yaml` for service configuration
- `Procfile` for start command
- Environment variables set in Render dashboard

### Frontend (Vercel)
The Next.js frontend is deployed on Vercel with:
- Automatic deployments from main branch
- Environment variables configured in Vercel dashboard
- API URL pointing to Render backend

---

## 💡 Usage Examples

### Example 1: Skincare Product
```
Query: "best vitamin c serum for brightening skin"
Product: "Minimalist"
Competitor: "Drunk Elephant"
```

### Example 2: SaaS Tool
```
Query: "best project management tool for small teams"
Product: "Notion"
Competitor: "Asana"
```

### Example 3: Food Product
```
Query: "healthiest protein bars for weight loss"
Product: "RXBAR"
Competitor: "Quest Bar"
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Ideas for Contributions
- Add more AI models
- Improve sentiment analysis accuracy
- Add historical tracking of AEO scores
- Create export functionality (PDF reports)
- Add more recommendation strategies

---

## 📝 License

This project is open-source. Feel free to use it for your own projects!

---

## 🙏 Acknowledgments

- [OpenRouter](https://openrouter.ai/) for providing access to multiple LLMs
- [Google Gemini](https://ai.google.dev/) for their generative AI API
- [shadcn/ui](https://ui.shadcn.com/) for beautiful UI components
- [Vercel](https://vercel.com/) for seamless frontend deployment
- [Render](https://render.com/) for reliable backend hosting

---

<p align="center">
  Built with ❤️ by <a href="https://github.com/sarthaksenapati">Sarthak Senapati</a>
</p>

<p align="center">
  ⭐ Star this repo if you find it useful!
</p>
