# Chat with Website 🌐

A Streamlit application that allows you to chat with any website content using Google's Gemini AI. Simply enter a website URL, and the app will scrape, process, and enable you to ask questions about the content.

## Features

- **Web Scraping**: Automatically extracts content from any website
- **RAG Implementation**: Uses Retrieval-Augmented Generation with Gemini API
- **Interactive Chat**: Streamlit-based chat interface
- **Smart Chunking**: Intelligently splits content for better retrieval
- **Semantic Search**: Finds relevant content using embeddings

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

3. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Enter your Gemini API key in the sidebar
2. Input a website URL
3. Click "Load Website" to scrape and process content
4. Start asking questions about the website content!

## Project Structure

```
Chat-With-Website/
├── app.py              # Main Streamlit application
├── utils/
│   ├── web_scraper.py  # Website content extraction
│   ├── embedder.py     # Text chunking and embeddings
│   └── retriever.py    # RAG implementation
├── data/               # Processed website data
└── requirements.txt    # Dependencies
```