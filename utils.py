# utils.py
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from gtts import gTTS
import uuid
import os
import re

def fetch_articles(company_name):
    """
    Scrapes 10 news article titles and content from Bing News Search (non-JS links).
    """
    search_url = f"https://www.bing.com/news/search?q={company_name}&FORM=HDRSC6"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    results = []
    links = soup.find_all('a', href=True)

    seen_titles = set()
    for a in links:
        href = a['href']
        if "http" in href and "news" in href.lower():
            try:
                article = requests.get(href, timeout=5)
                article_soup = BeautifulSoup(article.content, 'html.parser')
                title = article_soup.title.text.strip()

                if title in seen_titles:
                    continue
                seen_titles.add(title)

                paragraphs = article_soup.find_all('p')
                content = " ".join([p.get_text() for p in paragraphs])
                content = re.sub(r'\s+', ' ', content)

                if len(content) > 300:
                    results.append({'title': title, 'content': content})
                if len(results) >= 10:
                    break
            except:
                continue
    return results


def summarize_content(content, max_sentences=3):
    sentences = content.split(". ")
    return ". ".join(sentences[:max_sentences]) + "." if len(sentences) >= max_sentences else content


def get_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"


def extract_topics(text, top_k=5):
    vectorizer = CountVectorizer(stop_words='english', max_features=top_k)
    X = vectorizer.fit_transform([text])
    keywords = vectorizer.get_feature_names_out()
    return [(kw, 1.0) for kw in keywords]


def comparative_analysis(articles):
    sentiments = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for article in articles:
        sentiments[article['Sentiment']] += 1

    coverage_diff = []
    topics_set = [set(article['Topics']) for article in articles]
    all_topics = [t for s in topics_set for t in s]

    for i in range(len(articles)):
        for j in range(i + 1, len(articles)):
            if i != j:
                comparison = f"{articles[i]['Title']} vs {articles[j]['Title']}"
                impact = f"{articles[i]['Sentiment']} sentiment vs {articles[j]['Sentiment']} sentiment."
                coverage_diff.append({"Comparison": comparison, "Impact": impact})

    common_topics = set.intersection(*topics_set) if topics_set else set()
    topic_overlap = {
        "Common Topics": list(common_topics),
        "Unique Topics in Article 1": list(topics_set[0] - common_topics) if topics_set else [],
        "Unique Topics in Article 2": list(topics_set[1] - common_topics) if len(topics_set) > 1 else [],
    }

    return {
        "Sentiment Distribution": sentiments,
        "Coverage Differences": coverage_diff[:3],  # limit for brevity
        "Topic Overlap": topic_overlap
    }


def convert_text_to_hindi_speech(text, lang='hi'):
    tts = gTTS(text, lang=lang)
    file_path = f"audio_{uuid.uuid4().hex}.mp3"
    tts.save(file_path)
    return file_path
