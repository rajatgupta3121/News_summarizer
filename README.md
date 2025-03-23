---

## 📢 **Company News Summarization & Sentiment Analysis App (with Hindi Audio)**  
##🚀 **Live Demo**: [Click here to use the app on Hugging Face Spaces](https://huggingface.co/spaces/rajatgupta3121/News_summarizer)  

---

### ✅ **Project Overview**  
In today’s fast-paced world, professionals, investors, and researchers need quick, actionable insights from scattered news sources. This AI-powered application helps users:  
- Fetch the latest news articles about any company  
- Generate intelligent summaries using transformer-based models  
- Analyze sentiment distribution across multiple articles  
- Compare coverage differences and detect topic overlaps  
- Get an auto-generated **Hindi audio summary** for localized understanding  

---

### ✅ **Key Features**  
| 🌟 Feature                               | Description                                                                          |
|------------------------------------------|--------------------------------------------------------------------------------------|
| ✅ News Extraction                       | Scrapes latest articles from Bing News about the entered company                    |
| ✅ Text Summarization                    | Summarizes long-form articles using Hugging Face’s **BART-large-CNN** model         |
| ✅ Sentiment Analysis                    | Uses **VADER Sentiment Analyzer** to classify article tone as Positive, Negative, or Neutral |
| ✅ Comparative Insights                  | Analyzes sentiment patterns, topic overlaps, and coverage differences               |
| ✅ Hindi Audio Summary                   | Generates spoken summary in Hindi using **gTTS (Google Text-to-Speech)**            |
| ✅ Visual Sentiment Distribution         | Pie chart visualization for easy analysis                                           |
| ✅ Gradio-based User Interface           | Deployed on Hugging Face Spaces for interactive usage                               |

---

### ✅ **Tech Stack & Tools Used**  
- Python 3.10  
- **BeautifulSoup** & **newspaper3k** for web scraping  
- **Hugging Face Transformers (BART-large-cnn)** for summarization  
- **VADER Sentiment Analyzer** for sentiment scoring  
- **gTTS** for Hindi text-to-speech audio generation  
- **Plotly** for interactive sentiment visualization  
- **Gradio** for building and deploying the frontend  
- Hosted on: **Hugging Face Spaces**  

---

### ✅ **How the Application Works**  
1. The user enters a company name.  
2. The app scrapes up to 10 recent news articles from Bing News.  
3. Each article is summarized using the BART model.  
4. Sentiment analysis is performed on each article using VADER.  
5. The app compiles a comparative sentiment report with topic overlap analysis.  
6. A Hindi audio summary of the overall sentiment is generated and provided.  
7. All results are presented interactively on the Gradio interface with visual plots.  

---

### ✅ **Project Structure**
```
├── app.py                   # Gradio application file
├── utils.py                 # Backend functions: scraping, summarization, sentiment analysis, TTS
├── requirements.txt         # List of dependencies for Hugging Face Spaces
├── huggingface.yaml         # Deployment configuration for Hugging Face
└── README.md                # Project documentation (this file)
```

---

### ✅ **Installation (if running locally)**
```bash
git clone https://github.com/rajatgupta3121/News_summarizer.git
cd News_summarizer
pip install -r requirements.txt
python app.py
```

---

### ✅ **Live Demo**
👉 Try the app live on Hugging Face Spaces:  
➡️ [https://huggingface.co/spaces/rajatgupta3121/News_summarizer](https://huggingface.co/spaces/rajatgupta3121/News_summarizer)  

---

### ✅ **Next Improvements (Roadmap)**
- Add PDF report export  
- Daily email alerts for company-specific sentiment summaries  
- Multilingual audio generation (English + Hindi)  
- User authentication for tracking saved reports  

---

### 🙌 **Made with ❤️ by Rajat Gupta**  
> For collaboration or queries:  
📧 Email: [rajatgupta46300@gmail.com]  
🌐 GitHub: [https://github.com/rajatgupta3121](https://github.com/rajatgupta3121)  

