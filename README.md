# 📰 News Summarization and Hindi Text-to-Speech Web App

This project is a full-stack web application that allows users to:
- Enter a **company name**
- Scrape relevant news articles
- Perform **sentiment analysis** and **comparative analysis**
- Generate **summarized insights**
- Convert the final report to **Hindi speech output**

---

## 🚀 Features
- 📄 Web scraping of live news data
- 🧠 Sentiment and comparative analysis using NLP
- 📊 Summary report in JSON
- 🔈 Hindi text-to-speech generation
- 🌐 Deployed via Streamlit (frontend) and FastAPI (backend)

---

# 🛠️ Technologies Used
Python 3.11+

Streamlit

FastAPI

BeautifulSoup (for scraping)

spaCy

Sentence Transformers

gTTS (for Hindi speech)

Transformers (Hugging Face)

---
  
# Create Virtual Environment
python -m venv .venv
.venv\Scripts\activate   # On Windows

---

# Install Requirements
pip install -r requirements.txt
python -m textblob.download_corpora

---

# Run the Application
Run backend:
uvicorn main:app --reload
Run frontend:
streamlit run app.py

---

# 💻 Usage

Enter a company name in the Streamlit UI.

It scrapes relevant news from the internet.

Performs summarization, sentiment, and comparative analysis.

Generates a Hindi audio file (news_audio.mp3).

Displays interactive analysis results.

---
