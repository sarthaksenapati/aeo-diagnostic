from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

app = FastAPI()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

async def ask_llm(query: str, model: str, model_name: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": query}]
            },
            timeout=30.0
        )
        data = response.json()
        print(f"\n--- {model_name} response ---")
        print(data)
        print("---")
        text = data["choices"][0]["message"]["content"]
        return {"model": model_name, "response": text}

def analyze_ranking(response: str, product: str) -> dict:
    response_lower = response.lower()
    product_lower = product.lower()
    mentioned = product_lower in response_lower

    if mentioned:
        position = response_lower.find(product_lower)
        total_length = len(response_lower)
        if position < total_length * 0.3:
            rank = "Top mention"
            score = 10
        elif position < total_length * 0.6:
            rank = "Middle mention"
            score = 6
        else:
            rank = "Late mention"
            score = 3
    else:
        rank = "Not mentioned"
        score = 0

    return {"mentioned": mentioned, "rank": rank, "score": score}

@app.post("/analyze")
async def analyze(request: dict):
    query = request["query"]
    product = request["product"]

    models = [
        ("tencent/hy3-preview:free", "Hunyuan"),
        ("nvidia/nemotron-3-super-120b-a12b:free", "Nemotron 120B"),
        ("openai/gpt-oss-120b:free", "GPT OSS 120B"),
    ]
    tasks = [ask_llm(query, model_id, name) for model_id, name in models]
    responses = await asyncio.gather(*tasks)

    results = {}
    for r in responses:
        results[r["model"]] = {
            "response": r["response"],
            "analysis": analyze_ranking(r["response"], product)
        }

    return {
        "query": query,
        "product": product,
        "results": results
    }