
<div align="center">

# 📊 Financial Data Extractor

### *Turn Unstructured Earnings Reports & PDFs into Structured Intelligence — Instantly.*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-LCEL-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)](https://www.langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.3%2070B-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

<br/>

> ⚡ **Stop manually scanning earnings reports. Extract financial insights in seconds.**

<br/>

<img width="1874" height="685" alt="image" src="https://github.com/user-attachments/assets/491aba35-bb8c-41e2-95e9-9cd0c367d7a2" />
<img width="1860" height="391" alt="image" src="https://github.com/user-attachments/assets/2ec90e97-f87a-4435-8d11-312cd2677331" />


</div>

---

## 🔍 Overview

**Financial Data Extractor** is a production-ready AI tool that converts **unstructured financial text and PDFs** into **structured, validated financial data**.

It eliminates manual effort for analysts by extracting:

- Revenue (Actual vs Expected)
- EPS (Actual vs Expected)
- Revenue Growth
- Segment-wise Revenue Breakdown
- Source Evidence (verifiable quote)

---

## ✨ Features

- ⚡ **Instant Extraction** — Powered by Groq LPU™ for ultra-fast inference  
- 📄 **PDF + Text Support** — Upload earnings reports directly  
- 🛡️ **Strict Validation** — Pydantic ensures clean, reliable JSON  
- 📊 **Beat / Miss Analysis** — Auto comparison of actual vs expected  
- 🧩 **Revenue Bifurcation** — Segment-level breakdown  
- 🔍 **Source Transparency** — Extracts exact supporting quote  
- 📥 **CSV Export** — Download structured data instantly  
- 🎨 **FinTech UI** — Clean Streamlit dashboard  

---

## 🏗️ Architecture

```text
User Input (PDF / Text)
        │
        ▼
Streamlit UI (main.py)
        │
        ▼
LangChain LCEL Pipeline
(Prompt → LLM → Structured Output)
        │
        ▼
Groq (Llama 3.3 70B)
        │
        ▼
Validated JSON (Pydantic)
        │
        ▼
Dashboard + CSV Export
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|------|-----------|
| Language | Python 3.10+ |
| AI Orchestration | LangChain (LCEL) |
| LLM | Llama 3.3 70B (Groq) |
| Validation | Pydantic |
| PDF Parsing | pdfplumber |
| Frontend | Streamlit |
| Config | python-dotenv |

---

## 🚀 Getting Started

### 1. Clone Repo
git clone https://github.com/savera1226/financial-data-extractor.git  
cd financial-data-extractor  

### 2. Install Dependencies
pip install -r requirements.txt  

### 3. Add API Key
Create a `.env` file in the root directory:

GROQ_API_KEY=your_api_key_here  

### 4. Run App
streamlit run main.py  

Open in browser: http://localhost:8501  

---

## 💡 How It Works

1. Upload or paste financial text / earnings report  
2. Click **Extract Data ⚡**  
3. AI processes using LangChain + Groq  
4. Get structured financial insights instantly  

---

## 📊 Sample Output

| Metric | Expected | Actual |
|--------|---------|--------|
| Revenue | $109.0B | $113.8B |
| EPS | $2.64 | $2.82 |

### Revenue Breakdown
- Google Services — $95.9B  
- Search — $63.1B  
- YouTube Ads — $11.4B  
- Cloud — $17.7B  

---

## 📁 Project Structure

financial-data-extractor/  
│  
├── main.py  
├── data_extractor.py  
├── requirements.txt  
├── .env  
├── .gitignore  
└── README.md  

---

## 🌐 Deployment (Streamlit Cloud)

1. Push code to GitHub  
2. Go to https://share.streamlit.io  
3. Select your repository and set `main.py` as entry point  
4. Add secret:

GROQ_API_KEY="your_api_key_here"  

5. Click Deploy ✅  

---

## 🔒 Security

- No data is stored or logged  
- Fully stateless processing  
- API keys handled via environment variables only  

---

## 🧭 Roadmap

- [x] Revenue Bifurcation  
- [x] PDF Upload  
- [x] CSV Export  
- [ ] Multi-document comparison  
- [ ] Multilingual support  
- [ ] REST API  

---

## 🤝 Contributing

1. Fork the repository  
2. Create a feature branch  
3. Commit your changes  
4. Push and open a Pull Request  

---

## 📄 License

MIT License — see LICENSE file  

---

## ⭐ Support

If this project helped you, consider giving it a ⭐ on GitHub!
