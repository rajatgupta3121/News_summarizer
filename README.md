# 📰 AI-Powered News Summarization & Sentiment Analysis Web App

## 🔍 Overview

This is a powerful and user-friendly **AI-based News Summarization Web Application** that helps users stay informed quickly and efficiently. The app fetches real-time news based on user input, summarizes it using advanced NLP techniques, analyzes the sentiment of the summaries, and even reads them out loud in **English or Hindi** via Text-to-Speech (TTS). The app is inclusive and interactive, featuring **voice search**, **Hindi language support**, and a **fallback web search** system.

---

## ✨ Key Features

✅ **Real-Time News Fetching**  
- Fetches current news from reliable sources based on user-entered keywords via News API.

✅ **Abstractive NLP Summarization**  
- Uses Natural Language Processing to generate concise, context-aware summaries of long news articles.

✅ **Sentiment Analysis**  
- Applies machine learning to detect and label news sentiment as *Positive, Negative, or Neutral*.

✅ **Text-to-Speech (TTS) Playback**  
- Converts English or Hindi summaries to speech using `gTTS`, helping visually impaired users or multitaskers.

✅ **Hindi Language Support**  
- Automatically translates English summaries into Hindi using the `googletrans` library for regional accessibility.

✅ **Voice Search Integration**  
- Accepts voice commands using `SpeechRecognition` and converts them to keyword-based queries.

✅ **Fallback Mechanism with Web Browser**  
- Opens a browser search when AI fails to generate meaningful output, ensuring users are never left without results.

---

## 🛠️ Technologies Used

| Purpose                | Technology/Library                |
|------------------------|-----------------------------------|
| Backend                | Python, Flask                     |
| Frontend               | HTML, CSS, JavaScript             |
| News API               | NewsAPI.org or similar            |
| Summarization          | Transformers (e.g., BART/T5), or custom NLP logic |
| Sentiment Analysis     | VADER or Custom Trained Classifier|
| Text-to-Speech         | gTTS                              |
| Translation            | googletrans                       |
| Voice Input            | SpeechRecognition, PyAudio        |
| Fallback Search        | Python `webbrowser` library       |

---

## 📦 Installation & Setup

### 🔧 Prerequisites
- Python 3.7+
- pip
- Internet connection (for APIs)

### 🖥️ Clone the Repository
```bash
git clone https://github.com/rajatgupta3121/News_summarizer.git
cd news_summarizer
```

### 📥 Install Dependencies
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install flask gtts googletrans==4.0.0-rc1 speechrecognition requests beautifulsoup4 transformers torch
```

### 🔑 API Key Setup
1. Go to [NewsAPI.org](https://newsapi.org/)
2. Sign up and get your API key
3. Replace `YOUR_API_KEY` in your code (typically in `news_fetcher.py` or similar file)

### 🚀 Run the App
```bash
python app.py
```

Visit `http://127.0.0.1:5000/` in your browser.

---

## 🎯 Project Objectives & Results

| Objective | Outcome |
|----------|---------|
| Real-Time News Fetching | ✅ Successfully integrated API and retrieved relevant news |
| NLP Summarization | ✅ Meaningful, concise summaries generated |
| Sentiment Analysis | ✅ Sentiments correctly classified |
| Text-to-Speech | ✅ English & Hindi playback worked flawlessly |
| Hindi Support | ✅ Translated summaries for regional users |
| Voice Search | ✅ Accurate voice-to-text search |
| Fallback Search | ✅ Opens web browser if no result found |

---

## 🚀 Future Enhancements

- Add user authentication and history tracking  
- Allow users to save or share summaries  
- Extend support to more Indian languages  
- Add mobile app version using React Native or Flutter  
- Improve summarization with larger transformer models

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 📬 Contact

Developed by: **[Rajat Gupta]**  
📧 Email: rajatgupta46300@gmail.com  
🔗 LinkedIn: [linkedin.com/in/yourprofile](https://www.linkedin.com/in/rajat-gupta-b86a58268/)  
🌐 Portfolio: [yourportfolio.com](https://rajat-gupta-portfolio.netlify.app/)

---

