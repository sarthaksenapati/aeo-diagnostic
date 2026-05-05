from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODELS = [
    ("gemma-3-27b-it", "Gemma 3 27B"),
    ("nvidia/nemotron-3-super-120b-a12b:free", "Nemotron 3 Super"),
    ("openai/gpt-oss-120b:free", "GPT OSS 120B"),
]

POSITIVE_WORDS = ["best", "top", "excellent", "great", "highly recommended",
                  "superior", "outstanding", "perfect", "ideal", "trusted",
                  "popular", "effective", "quality", "recommended", "leading"]

NEGATIVE_WORDS = ["avoid", "poor", "bad", "worst", "inferior", "overpriced",
                  "disappointing", "mediocre", "unreliable", "cheap", "low quality"]

async def ask_llm(query: str, model: str, model_name: str) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            if model.startswith("gemini"):
                response = await client.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}",
                    headers={"Content-Type": "application/json"},
                    json={"contents": [{"parts": [{"text": query}]}]},
                    timeout=None
                )
                data = response.json()
                print(f"[{model}] STATUS: {response.status_code}")
                print(f"[{model}] RESPONSE: {data}")
                if "candidates" not in data:
                    return {"model": model_name, "response": f"Error: {data}", "error": True}
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return {"model": model_name, "response": text, "error": False}
            else:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://aeo-diagnostic.app",
                        "X-Title": "AEO Diagnostic"
                    },
                    json={
                        "model": model,
                        "messages": [{"role": "user", "content": query}],
                        
                    },
                    timeout=None
                )
                data = response.json()
                print(f"[{model}] STATUS: {response.status_code}")
                print(f"[{model}] RESPONSE: {data}")
                if "choices" not in data:
                    return {"model": model_name, "response": f"Error: {data}", "error": True}
                text = data["choices"][0]["message"]["content"]
                return {"model": model_name, "response": text, "error": False}

        except Exception as e:
            print(f"[{model}] EXCEPTION: {str(e)}")
            return {"model": model_name, "response": f"Error: {str(e)}", "error": True}

def analyze_ranking(response: str, product: str) -> dict:
    response_lower = response.lower()
    product_lower = product.lower()
    
    # Generate multiple variants to search for
    variants = [
        product_lower,
        product_lower.replace("&", "and"),
        product_lower.replace("and", "&"),
        product_lower.replace(" ", ""),      # "h&m" -> "hm"
        product_lower.replace("&", " and "), # "h&m" -> "h and m"
        product_lower.replace("-", " "),     # "coca-cola" -> "coca cola"
    ]
    # Remove duplicates
    variants = list(set(v.strip() for v in variants))
    
    # Check all variants
    mentioned = any(v in response_lower for v in variants if v)
    
    # Find position using whichever variant matched
    position = -1
    for v in variants:
        if v and v in response_lower:
            position = response_lower.find(v)
            break
    
    if mentioned and position != -1:
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

        window_start = max(0, position - 200)
        window_end = min(len(response_lower), position + 200)
        context = response_lower[window_start:window_end]

        pos_hits = sum(1 for w in POSITIVE_WORDS if w in context)
        neg_hits = sum(1 for w in NEGATIVE_WORDS if w in context)

        if pos_hits > neg_hits:
            sentiment = "Positive"
            sentiment_emoji = "😊"
        elif neg_hits > pos_hits:
            sentiment = "Negative"
            sentiment_emoji = "😟"
            score = max(0, score - 3)
        else:
            sentiment = "Neutral"
            sentiment_emoji = "😐"
    else:
        rank = "Not mentioned"
        score = 0
        sentiment = "Not mentioned"
        sentiment_emoji = "❌"

    return {
        "mentioned": mentioned,
        "rank": rank,
        "score": score,
        "sentiment": sentiment,
        "sentiment_emoji": sentiment_emoji
    }

def generate_recommendations(product: str, competitor: str, results: dict) -> list:
    recommendations = []
    scores = [r["analysis"]["score"] for r in results.values()]
    avg_score = sum(scores) / len(scores)

    if avg_score == 0:
        recommendations.append(f"'{product}' was not mentioned by any AI model. AI models recommend based on ingredient types and categories, not brand names. Ensure your product content clearly states its key ingredients and benefits.")
        recommendations.append("Consider creating detailed product descriptions that match common customer search queries.")
        recommendations.append("Build more online presence — reviews, articles, and mentions help AI models learn about your brand.")
    elif avg_score < 5:
        recommendations.append(f"'{product}' has low AI visibility. It appears late in responses, meaning AI considers it a secondary option.")
        recommendations.append("Focus on getting more third-party reviews and mentions on health/wellness websites.")
    else:
        recommendations.append(f"'{product}' has good AI visibility. Maintain your online presence and keep collecting reviews.")

    if competitor:
        comp_scores = [r["competitor_analysis"]["score"] for r in results.values() if "competitor_analysis" in r]
        if comp_scores:
            comp_avg = sum(comp_scores) / len(comp_scores)
            if comp_avg > avg_score:
                recommendations.append(f"Your competitor '{competitor}' outranks you (score: {comp_avg:.1f} vs {avg_score:.1f}). Study their product descriptions and marketing language.")
            elif avg_score > comp_avg:
                recommendations.append(f"You outrank '{competitor}' (score: {avg_score:.1f} vs {comp_avg:.1f}). Keep doing what you're doing!")
            else:
                recommendations.append(f"You and '{competitor}' are neck and neck. Small improvements in product content could tip the balance.")

    return recommendations

@app.post("/analyze")
async def analyze(request: dict):
    query = request["query"]
    product = request["product"]
    competitor = request.get("competitor", "")

    # Wrap the query in a realistic prompt
    prompt = f"""A customer asked: "{query}"

Answer this as a helpful AI shopping assistant. Be specific — recommend actual brand names, explain why each is good, and rank them if possible. Give a natural, conversational response like ChatGPT or Perplexity would."""

    tasks = [ask_llm(prompt, model_id, name) for model_id, name in MODELS]
    responses = await asyncio.gather(*tasks)

    results = {}
    for r in responses:
        if r.get("error"):
            continue
        analysis = analyze_ranking(r["response"], product)
        entry = {
            "response": r["response"],
            "analysis": analysis
        }
        if competitor:
            entry["competitor_analysis"] = analyze_ranking(r["response"], competitor)
        results[r["model"]] = entry

    scores = [r["analysis"]["score"] for r in results.values()]
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0

    recommendations = generate_recommendations(product, competitor, results)

    return {
        "query": query,
        "product": product,
        "competitor": competitor,
        "results": results,
        "avg_score": avg_score,
        "recommendations": recommendations
    }
