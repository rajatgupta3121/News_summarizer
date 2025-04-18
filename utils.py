import requests
from bs4 import BeautifulSoup
from newspaper import Article
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from gtts import gTTS
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import random
import time

vader_analyzer = SentimentIntensityAnalyzer()

# Multiple browser user-agents for rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:117.0) Gecko/20100101 Firefox/117.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1'
]

def get_random_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS)
    }

# --- Fetch articles with retry and fallback selectors ---
def fetch_articles_for_company(company, start_date=None, end_date=None, keywords="", source="All", attempts=2):
    articles = []
    
    # Format date range if provided
    date_query = ""
    if start_date and end_date:
        try:
            start = datetime.strptime(str(start_date), "%Y-%m-%d").strftime("%Y-%m-%d")
            end = datetime.strptime(str(end_date), "%Y-%m-%d").strftime("%Y-%m-%d")
            date_query = f" after:{start} before:{end}"
        except:
            pass

    keyword_query = f" {keywords}" if keywords else ""
    source_query = f" site:{source.lower().replace(' ', '')}.com" if source != "All" else ""

    query = f"{company}{keyword_query}{source_query}{date_query}"
    search_url = f"https://www.bing.com/news/search?q={query}&FORM=HDRSC6"

    for attempt in range(attempts):
        try:
            response = requests.get(search_url, headers=get_random_headers(), timeout=8)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            items = soup.select("a.title")
            if not items:
                items = soup.select("a.news-card__title")
            if not items:
                items = soup.find_all("a", {"target": "_blank"})

            if items:
                with ThreadPoolExecutor(max_workers=4) as executor:
                    futures = [
                        executor.submit(fetch_article_content, item["href"], item.get_text(strip=True))
                        for item in items[:20]
                        if item.get("href", "").startswith("http")
                    ]
                    for future in futures:
                        result = future.result()
                        if len(result["content"].split()) > 10:
                            articles.append(result)

            if articles:
                break
            else:
                time.sleep(1)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(1)

    if not articles:
        articles.append({
            "title": "No articles found. Bing structure may have changed or no recent news.",
            "url": "",
            "content": "No content available."
        })

    return articles


# --- Fetch single article content with fallback ---
def fetch_article_content(url, title):
    content = ""
    try:
        article = Article(url)
        article.download()
        article.parse()
        content = article.text.strip()
    except:
        pass

    # Fallback scraping if too short
    if len(content.split()) < 15:
        try:
            fallback_res = requests.get(url, headers=get_random_headers(), timeout=5)
            fallback_soup = BeautifulSoup(fallback_res.content, "html.parser")
            paragraphs = fallback_soup.find_all('p')
            if not paragraphs:
                divs = fallback_soup.find_all('div')
                paragraphs = [div for div in divs if len(div.get_text(strip=True)) > 50]
            content = " ".join([p.get_text() for p in paragraphs]).strip()
        except:
            content = "Content unavailable."

    return {"title": title, "url": url, "content": content}

# --- Fast summarization using sumy (LSA) ---
def generate_summary_fast(text):
    if not text or len(text.strip().split()) < 50:
        return text.strip()[:250] + "..." if text else "Summary not available."
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary_sentences = summarizer(parser.document, sentences_count=3)
        return " ".join(str(sentence) for sentence in summary_sentences)
    except:
        return text[:300] + "..."

# --- Sentiment analysis using VADER ---
def analyze_sentiment_vader(text):
    scores = vader_analyzer.polarity_scores(text)
    comp = scores['compound']
    if comp >= 0.05:
        return "Positive"
    elif comp <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# --- Comparative analysis report ---
def comparative_analysis(articles):
    sentiment_dist = {"Positive": 0, "Negative": 0, "Neutral": 0}
    keywords = []

    for article in articles:
        sentiment_dist[article['sentiment']] += 1
        headline_words = article['title'].split(" ")[:2]
        keywords.extend(headline_words)

    overall_sentiment = (
        "mostly positive" if sentiment_dist["Positive"] > sentiment_dist["Negative"] else "mixed or negative"
    )

    return {
        "Sentiment Distribution": sentiment_dist,
        "Coverage Differences": [
            {"Comparison": "Some articles show optimism, others show caution.", "Impact": "Mixed sentiment perception."}
        ],
        "Topic Overlap": {
            "Common Keywords": list(set(keywords))
        },
        "Overall Sentiment Conclusion": overall_sentiment
    }

# --- Generate Hindi TTS in-memory ---
def generate_hindi_tts_bytes(text):
    try:
        tts = gTTS(text=text, lang='hi')
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes
    except:
        return None

# --- Parallel summary & sentiment processing ---
def process_article(article):
    content = article.get('content', '')
    article['summary'] = generate_summary_fast(content)
    article['sentiment'] = analyze_sentiment_vader(content)
    return article

def process_articles_parallel(articles):
    with ThreadPoolExecutor(max_workers=4) as executor:
        return list(executor.map(process_article, articles))

