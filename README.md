# 🎬 Movie Information Extraction Bot

An AI-powered web application that extracts structured movie metadata (such as Movie Name, Cast, Director, Release Year, Plot, Themes, Setting, Keywords, and Summary) strictly from user-provided text paragraphs without hallucinating or making external assumptions.

Powered by **FastAPI**, **LangChain**, and **Groq Cloud LLMs**, optimized for seamless one-click deployment to **Vercel**.

---

## ✨ Features

- **Strict Extraction Engine**: Extracts only facts explicitly stated in the input text. Fields not present default to *"Not mentioned"*.
- **Modern Minimal UI**: Sleek, high-contrast dark theme with instant sample inputs and keyboard shortcuts (`Ctrl + Enter`).
- **Serverless Ready**: Configured with Vercel Serverless Python (`/api/index.py`), requiring zero external server configuration.
- **Fast Inference**: Powered by Groq ultra-low latency inference (using `llama-3.3-70b-versatile` or custom models).

---

## 🛠️ Tech Stack

- **Frontend**: HTML5, Vanilla CSS3 (Custom Glassmorphism & Dark Design), Modern JavaScript (ES6+)
- **Backend API**: FastAPI, Pydantic, Uvicorn
- **AI / LLM Orchestration**: LangChain Core, LangChain Groq
- **Deployment**: Vercel (Serverless Python Functions + Static Hosting)

---

## 🚀 Getting Started Locally

### 1. Clone the repository
```bash
git clone https://github.com/yoloaryan/Movie_extract.git
cd Movie_extract
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### 5. Run the application
```bash
python server.py
```
Open your browser and navigate to: `http://localhost:8000`

---

## ☁️ Deploying to Vercel

1. Push this repository to your GitHub account (`https://github.com/yoloaryan/Movie_extract`).
2. Go to [Vercel Dashboard](https://vercel.com/) and click **Add New Project**.
3. Import the `Movie_extract` repository.
4. Under **Environment Variables**, add:
   - `GROQ_API_KEY` = `your_groq_api_key`
   - *(Optional)* `GROQ_MODEL` = `llama-3.3-70b-versatile`
5. Click **Deploy**. Vercel will automatically build the static assets and the serverless Python API.

---

## 📄 License
MIT License. Free to use and modify.
