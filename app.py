# app.py
import streamlit as st
import requests

st.set_page_config(page_title="📰 News Summarization & Hindi Text-to-Speech", layout="centered")
st.title("📰 News Summarization & Hindi Text-to-Speech")

company = st.text_input("Enter a Company Name", "")

if st.button("Analyze") and company:
    with st.spinner("Analyzing news..."):
        try:
            response = requests.post("http://127.0.0.1:8000/analyze", json={"company": company})
            result = response.json()

            if "error" in result:
                st.error(result["error"])
            else:
                st.header(f"Sentiment Report for {result['Company']}")

                for article in result["Articles"]:
                    st.subheader(article["Title"])
                    st.write(f"**Summary:** {article['Summary']}")
                    st.write(f"**Sentiment:** {article['Sentiment']}")
                    st.write(f"**Topics:** {', '.join(article['Topics'])}")
                    st.markdown("---")

                st.subheader("🧠 Comparative Sentiment Analysis")
                st.json(result["Comparative Sentiment Score"])

                st.success(result["Final Sentiment Analysis"])

                st.subheader("🔊 Hindi Audio Summary")
                audio_path = result["Audio"]
                audio_bytes = open(audio_path, "rb").read()
                st.audio(audio_bytes, format="audio/wav")

        except Exception as e:
            st.error(f"Error: {e}")
