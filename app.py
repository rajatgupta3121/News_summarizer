import streamlit as st
import plotly.express as px
import base64
from datetime import datetime
from streamlit_lottie import st_lottie
import json
import requests
from utils import (
    fetch_articles_for_company,
    generate_summary_fast,
    analyze_sentiment_vader,
    generate_hindi_tts_bytes,
    process_articles_parallel
)

st.set_page_config(page_title="⚡ Ultra-Fast Company News Summarizer", layout="wide", page_icon="🗞️")

# Load Lottie animation
@st.cache_data
def load_lottie_animation():
    url = "https://assets10.lottiefiles.com/packages/lf20_qp1q7mct.json"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        return None

lottie_anim = load_lottie_animation()


# Theme Toggle
mode = st.sidebar.radio("Select Theme", ["Light", "Dark"])
if mode == "Dark":
    background_color = "#1e1e1e"
    text_color = "#ffffff"
    card_color = "#2c2c2c"
else:
    background_color = "#f4f7fa"
    text_color = "#2C3E50"
    card_color = "#968d8d"

# Custom Styling
st.markdown(f"""
    <style>
        body {{
            background-color: {background_color};
            color: {text_color};
        }}
        .main-title {{
            font-size: 3.5em;
            font-weight: 800;
            text-align: center;
            color: {text_color};
            margin-top: 20px;
            margin-bottom: 30px;
            animation: fadeIn 2s ease;
        }}
        .stButton > button {{
            background: linear-gradient(90deg, #4CAF50, #81C784);
            color: white;
            font-size: 1.2em;
            border: none;
            border-radius: 12px;
            padding: 12px 28px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease-in-out;
        }}
        .stButton > button:hover {{
            transform: scale(1.05);
        }}
        .card {{
            background-color: {card_color};
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            transition: 0.3s ease;
        }}
        .card:hover {{
            transform: scale(1.02);
        }}
        @keyframes fadeIn {{
            from {{opacity: 0; transform: translateY(-10px);}}
            to {{opacity: 1; transform: translateY(0);}}
        }}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📰 News Summarizer & Sentiment Insights</div>', unsafe_allow_html=True)

# Intro container with Lottie animation
with st.container():
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
            Welcome to the Ultra-Fast News Summarizer App!
            - 🔍 Enter a company name
            - 📅 Choose your date range
            - 📈 Analyze sentiment
            - 🎧 Hear it in Hindi!
        """)
    with col2:
        if lottie_anim:
            st_lottie(lottie_anim, height=180, key="intro")

# Sidebar Inputs
with st.sidebar:
    st.header("🔧 Filters")
    company = st.text_input("Company Name")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    keywords = st.text_input("Keywords (comma separated)")
    source = st.selectbox("News Source", ["All", "Google News", "Yahoo Finance", "Reuters"])
    sentiment_filter = st.slider("Sentiment Intensity", -1.0, 1.0, (-1.0, 1.0))
    sort_option = st.selectbox("Sort By", ["Relevance", "Recency", "Sentiment"])
    analyze = st.button("🔎 Analyze")

if analyze:
    if company.strip() == "":
        st.error("⚠️ Please enter a company name.")
    else:
        with st.spinner("⏳ Fetching and analyzing the articles..."):
            articles = fetch_articles_for_company(company, start_date=start_date, end_date=end_date, keywords=keywords, source=source)
            articles = process_articles_parallel(articles)

            if not articles:
                st.error(f"❌ No articles found for {company}.")
            else:
                filtered_articles = [a for a in articles if 'compound' not in a or sentiment_filter[0] <= a['compound'] <= sentiment_filter[1]]

                if sort_option == "Sentiment":
                    filtered_articles.sort(key=lambda x: x.get('compound', 0), reverse=True)
                elif sort_option == "Recency":
                    filtered_articles.sort(key=lambda x: x.get('publishedAt', ''), reverse=True)

                final_sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
                for article in filtered_articles:
                    final_sentiment_counts[article['sentiment']] += 1

                final_sentiment = max(final_sentiment_counts, key=final_sentiment_counts.get)

                audio_bytes = generate_hindi_tts_bytes(
                    f"{company} ke news coverage ke anusar overall sentiment {final_sentiment} hai."
                )

                st.subheader("📊 Sentiment Distribution")
                fig = px.pie(
                    names=list(final_sentiment_counts.keys()),
                    values=list(final_sentiment_counts.values()),
                    hole=0.4,
                    title="Sentiment Distribution",
                    color_discrete_map={
                        "Positive": "#28a745",
                        "Neutral": "#ffc107",
                        "Negative": "#dc3545"
                    }
                )
                st.plotly_chart(fig, use_container_width=True)

                st.subheader("📝 Article Summaries")
                for article in filtered_articles:
                    with st.container():
                        st.markdown(f"""
                        <div class='card'>
                            <h4>{article['title']}</h4>
                            <p><strong>Summary:</strong> {article['summary']}</p>
                            <p><strong>Sentiment:</strong> {article['sentiment']}</p>
                            <a href="{article['url']}" target="_blank">🔗 Read Full Article</a>
                        </div>
                        """, unsafe_allow_html=True)

                st.subheader("📌 News Insight Highlight")
                st.markdown(f"The sentiment trend across articles suggests that the most dominant tone in {company}'s recent news is **{final_sentiment}**.")

                st.subheader("🔊 Hindi Audio Summary")
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3")
                    b64_audio = base64.b64encode(audio_bytes.read()).decode()
                    download_link = f'<a href="data:audio/mp3;base64,{b64_audio}" download="{company}_summary.mp3">📥 Download Hindi Audio Summary</a>'
                    st.markdown(download_link, unsafe_allow_html=True)
                else:
                    st.warning("Audio generation failed.")

st.markdown("---")
st.caption("Crafted with ❤️ by Rajat Gupta 🚀")
