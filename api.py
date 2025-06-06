# api.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from utils import (
    fetch_articles,
    summarize_content,
    get_sentiment,
    extract_topics,
    comparative_analysis,
    convert_text_to_hindi_speech,
)
import uvicorn
import traceback

app = FastAPI()

# CORS middleware for frontend-backend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(request: Request):
    try:
        data = await request.json()
        company = data.get("company")
        if not company:
            return {"error": "No company name provided."}

        print(f"[INFO] Fetching articles for: {company}")
        articles_raw = fetch_articles(company)

        if not articles_raw:
            return {"error": "No articles found for the given company."}

        articles_data = []
        for article in articles_raw:
            summary = summarize_content(article['content'])
            sentiment = get_sentiment(article['content'])
            topics = [kw[0] for kw in extract_topics(article['content'])]
            articles_data.append({
                "Title": article['title'],
                "Summary": summary,
                "Sentiment": sentiment,
                "Topics": topics
            })

        comparison = comparative_analysis(articles_data)
        top_sentiment = max(
            comparison['Sentiment Distribution'],
            key=comparison['Sentiment Distribution'].get
        )
        final_sentiment = f"{company}’s latest news coverage is mostly {top_sentiment}."

        hindi_text = f"{company} ke baare mein samacharon ka saar yeh hai: {final_sentiment}"
        audio_path = convert_text_to_hindi_speech(hindi_text)

        return {
            "Company": company,
            "Articles": articles_data,
            "Comparative Sentiment Score": comparison,
            "Final Sentiment Analysis": final_sentiment,
            "Audio": audio_path
        }

    except Exception as e:
        traceback.print_exc()
        return {"error": f"Internal Server Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
