# [🤗Hugging Face Deployed Streamlit App Link](https://huggingface.co/spaces/NeonSamurai/ITC-Financial-Analyzer)

# ITC Financial Analysis

This project analyzes ITC Ltd's revenue trends, profitability, and financial health using scraped financial data and Large Language Models (LLMs). It combines modern scraping tools (Tavily), embeddings, and LLMs to provide answers with source citations.

### 🚀 Features

- 🔍 **Automated Scraping**: Real-time financial data collection using Firecrawl or Crew AI.
- 🧠 **Embeddings**: Converts textual data into vector embeddings for intelligent querying.
- 💬 **LLM Integration**: Ask natural language questions and get answers backed by financial data.
- 🖥 **Streamlit App**: A simple, interactive UI for financial insights.

## Project Structure

This repository follows a modular structure to separate different components of the project. Below is the breakdown of the project flow:

```bash
itc-financial-analysis/  
├── scraper/              # Tavily scripts for scraping financial data
├── database/             # Used ChromaDB for storing and processing data along with Embeddings
├── embeddings/           # Code for embedding generation and document chunking
├── llm/                  # Code for handling LLM queries and integration
├── app.py                # Streamlit UI for user interaction and Q&A
└── README.md             # Setup instructions, and usage details
```

## 📄 ITC Financial Documents Scraper

This module fetches and processes financial reports and presentations from the ITC Limited website using the Tavily API. It extracts the raw textual content from a list of PDF URLs and structures it as `langchain` Document objects with metadata.

### 📦 Features

- ✅ Downloads and extracts content from ITC's:
  - Annual Reports (2023,2024)
  - Quarterly Result Presentations (Q1 to Q4 for FY2023–FY2025)
  - Standalone and Consolidated Financial Results
- ✅ Uses `TavilyClient` for deep PDF content extraction (`extract_depth="advanced"`)
- ✅ Organizes content with source metadata for future use in NLP/LLMs

### 🛠 Requirements

Install the required dependencies:

```bash
pip install tavily langchain
```

## 🧠 Embedding Financial Documents with Chroma

This script loads pre-processed financial documents, splits them into chunks, creates embeddings using a SentenceTransformer model, and stores them in a persistent `Chroma` vector database for efficient similarity search and retrieval.

### 📦 Features

- 📄 Loads `LangChain`-formatted documents from a pickle file
- ✂️ Splits large documents into smaller chunks using `RecursiveCharacterTextSplitter`
- 🔍 Generates vector embeddings using `all-MiniLM-L6-v2` from `sentence-transformers`
- 🧱 Saves embeddings in a local `Chroma` vector store
- 🗂 Archives the database directory into a `.zip` file for easy sharing or storage

### 🛠 Requirements

Install the necessary packages:

```bash
pip install langchain chromadb sentence-transformers
```


## 🤖 LLM & Vector Search Integration

An interactive Streamlit chatbot powered by Google's Gemini LLM and LangChain, enabling precise Q&A on **ITC Ltd.’s financial performance** by leveraging AI-based scraping, embedding, and document retrieval.

### 🔍 Key Features

- 🌐 Integrates LangChain's Chroma vector store for contextual retrieval
- 🧠 Uses `Gemini 2.0 Flash` via `ChatGoogleGenerativeAI` for real-time financial Q&A
- 🧾 Retrieves relevant financial context using MMR-based vector similarity

### 🧰 Requirements

Install the required libraries:

```bash
pip install streamlit sentence-transformers langchain chromadb langchain-google-genai
```

## ITC Financial Analyst Streamlit App

This Streamlit app enables interactive financial Q&A for **ITC Ltd.** by leveraging a pre-built vector database and Google's Gemini LLM. It provides structured insights from earnings transcripts or financial documents using LangChain.

### 🚀 App Highlights

### 🎯 Purpose
- Answer user queries about ITC’s financials using transcript-based information.
- Deliver accurate, year-wise, metric-specific financial insights.
- Provide source transparency with linked documents for every response.

### 🧩 Core Components
- **Vector Search (Chroma + MMR):** Retrieves relevant transcript sections.
- **LLM Integration (Gemini 2.0 Flash):** Interprets and answers based strictly on retrieved content.
- **Memory Chat Buffer:** Preserves chat history throughout the session.

---

## 🛠 How to Run

1. Place your Chroma DB zip file in the working directory.
2. Replace:
   ```python
   API_key = "your api key"
   ```
---
### ⚙️ Setup Instructions

#### 1. Clone the Repository

```bash
git clone https://github.com/Suhaib-Aamer/itc-financial-analysis.git
cd itc-financial-analysis
```
#### 2. Install all dependencies

```bash
pip install -r requirements.txt
```

### 🧠 Tech Stack

- **`LangChain`** – Document processing, chains, and memory management
- **`ChromaDB`** – Local vector database for storing embeddings
- **`Google Gemini`** – LLM inference via `ChatGoogleGenerativeAI`
- **`SentenceTransformers`** – Text embeddings using `all-MiniLM-L6-v2`
- **`Streamlit`** – Frontend UI framework for interactive applications
- **`Tavily`** – Deep PDF scraping and content extraction
