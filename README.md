# AEO Diagnostic Tool 🔍

See how your product ranks when AI assistants answer customer questions.

## Live Demo
👉 [Try it here](https://sarthaksenapati-aeo-diagnostic-frontend-enxsn8.streamlit.app)

## What it does
Paste any customer query and your brand name. 
The tool queries 3 AI models simultaneously and tells you 
whether your product gets recommended — and how prominently.

## Tech Stack
- FastAPI backend deployed on Render
- Streamlit frontend deployed on Streamlit Cloud
- 3 LLMs via OpenRouter API (Hunyuan, Nemotron 120B, GPT OSS 120B)
- Async parallel requests using asyncio

## Run locally
pip install -r requirements.txt
uvicorn main:app --reload
streamlit run frontend.py