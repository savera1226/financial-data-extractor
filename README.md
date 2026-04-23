<div align="center">

# 📊 Financial Data Extractor

### *Turning Unstructured Earnings Reports into Structured Intelligence — Instantly.*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-LCEL-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)](https://www.langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.3%2070B-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/savera1226/financial-data-extractor?style=for-the-badge)](https://github.com/savera1226/financial-data-extractor/stargazers)

<br/>

> **Analysts spend hours hunting through earnings calls and financial filings for key metrics.**
> This tool does it in **seconds.**

<br/>

<!-- 💡 Replace the line below with an actual screenshot or GIF of your running app -->
<!-- Example: ![App Demo](assets/demo.gif) -->

</div>

---

## 🔍 What Is This?

**Financial Data Extractor** is a production-ready AI application that automatically parses unstructured financial documents — earnings reports, press releases, news articles — and returns structured key metrics like **Revenue** and **EPS** with zero manual effort.

Built on **LangChain's LCEL pipeline** and powered by **Llama 3.3 70B via Groq's ultra-fast LPU™ inference**, this tool transforms the way investors, analysts, and fintech teams interact with financial data.

---

## ✨ Key Features

| Feature | Description |
|:---|:---|
| ⚡ **Sub-Second Inference** | Groq LPU™ hardware delivers near-instant LLM responses |
| 🧠 **Context-Aware Extraction** | Llama 3.3 70B understands financial meaning, not just keywords |
| 📄 **Unstructured → Structured** | Converts raw text into clean Revenue & EPS JSON |
| 🎨 **Custom Dark Mode UI** | Sleek Streamlit interface built for finance professionals |
| 🔒 **Privacy by Design** | No data is stored — all extractions run fully in-memory |
| 🔌 **Modular Architecture** | Clean separation of UI and AI logic for easy extension |

---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────┐
│                  Streamlit UI                    │
│         (main.py — Custom Dark Mode)             │
└────────────────────┬────────────────────────────┘
                     │ Raw Financial Text
                     ▼
┌─────────────────────────────────────────────────┐
│           LangChain LCEL Pipeline                │
│              (data_extractor.py)                 │
│                                                  │
│   PromptTemplate → ChatGroq → JsonOutputParser   │
└────────────────────┬────────────────────────────┘
                     │ Structured JSON
                     ▼
┌─────────────────────────────────────────────────┐
│         Groq Cloud — Llama 3.3 70B              │
│       (High-performance LPU™ inference)          │
└─────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|:---|:---|:---|
| **Language** | Python 3.10+ | Core runtime |
| **AI Orchestration** | LangChain (LCEL) | Chain composition & prompt management |
| **LLM** | Llama 3.3 70B via Groq | Financial entity extraction |
| **Frontend** | Streamlit + Custom CSS | Interactive dark-mode UI |
| **Config** | python-dotenv | Secure local API key management |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- A free [Groq API Key](https://console.groq.com/)

### 1. Clone the Repository
```bash
git clone https://github.com/savera1226/financial-data-extractor.git
cd financial-data-extractor
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Your API Key
Create a `.env` file in the root directory:
```plaintext
GROQ_API_KEY=your_actual_groq_api_key_here
```
> 🔐 The app loads this key via `load_dotenv()` at startup. Your key is **never hardcoded** and never leaves your machine during local development.

### 4. Launch the App
```bash
streamlit run main.py
```
The app will open at `http://localhost:8501` in your browser.

---

## 📁 Project Structure

```text
financial-data-extractor/
│
├── main.py               # Streamlit UI & custom dark-mode CSS
├── data_extractor.py     # LangChain LCEL chain & Groq integration
├── requirements.txt      # Pinned project dependencies
├── LICENSE               # MIT License
├── .env                  # API keys — local only, never commit this
├── .gitignore            # Excludes .env, __pycache__, .streamlit/
└── README.md             # Project documentation
```

### `.gitignore` (minimum recommended)
```gitignore
.env
__pycache__/
*.pyc
.streamlit/secrets.toml
```

### `requirements.txt` (recommended pinned versions)
```text
streamlit>=1.35.0
langchain>=0.2.0
langchain-groq>=0.1.6
python-dotenv>=1.0.0
```

---

## 💡 How It Works

1. **Paste** any earnings article, press release, or financial snippet into the input box
2. **Click "Extract"** — the LCEL chain sends your text through Llama 3.3 70B on Groq
3. **Receive** a clean JSON object with Revenue and EPS — ready to copy, export, or pipe downstream

```json
// Sample Output
{
  "revenue": "$4.2B",
  "eps": "$1.87"
}
```

---

## 🌐 Deploying to Streamlit Cloud

This app is **Streamlit Cloud ready.** No Docker, no DevOps, no servers.

1. Push your code to GitHub — confirm `.env` is **not** included
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **"New app"**, select your repo, and set `main.py` as the entry point
4. Navigate to **Advanced Settings → Secrets** and add:

```toml
GROQ_API_KEY = "your_actual_groq_api_key_here"
```

5. Click **Deploy** ✅

> ⚠️ Do **not** upload your `.env` file to GitHub. The Streamlit Secrets panel is the safe, correct way to inject API keys in the cloud.

---

## 🔒 Security

- All text processing is **stateless** — no user input is logged or persisted
- API keys are loaded via environment variables, never hardcoded in source
- The app holds no database, session storage, or external logging service
- Review [Groq's Privacy Policy](https://groq.com/privacy-policy/) for their inference data handling terms

---

## 🛠️ Troubleshooting

| Problem | Fix |
|:---|:---|
| `AuthenticationError` on startup | Verify `GROQ_API_KEY` is set in `.env` (local) or Streamlit Secrets (cloud) |
| `ModuleNotFoundError: langchain_groq` | Run `pip install langchain-groq` or reinstall from `requirements.txt` |
| App shows a blank page | Ensure `data_extractor.py` calls `load_dotenv()` before any `os.getenv()` call |
| Extraction returns `null` values | Input text may lack clear financial figures — try a real earnings press release |
| Port already in use | Run `streamlit run main.py --server.port 8502` to use an alternate port |

---

## 🔭 Roadmap

- [ ] **PDF Upload** — Drag-and-drop earnings PDFs for direct extraction
- [ ] **Multi-Model Support** — Switch between Llama, Mixtral, and Gemma on the fly
- [ ] **Excel / CSV Export** — One-click download of extracted metrics
- [ ] **Multilingual Support** — Extract from non-English financial filings
- [ ] **Batch Processing** — Analyze multiple reports in a single session
- [ ] **REST API Endpoint** — Trigger extractions programmatically via HTTP

---

## ✅ Pre-Deployment Checklist

### Local — Before Pushing to GitHub
- [x] `main.py`, `data_extractor.py`, and `requirements.txt` are present
- [x] `data_extractor.py` calls `load_dotenv()` before accessing environment variables
- [x] `.env` is listed in `.gitignore` and **not** staged for commit (`git status` to verify)
- [x] App runs without errors via `streamlit run main.py`

### Cloud — On Streamlit Share
- [ ] Repo is connected and `main.py` is set as the entry point
- [ ] `GROQ_API_KEY` is added under **Advanced Settings → Secrets**
- [ ] Deployment completes with no import or auth errors in the cloud logs

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

```bash
# 1. Fork the repo on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/financial-data-extractor.git

# 2. Create a feature branch
git checkout -b feat/your-feature-name

# 3. Make your changes, then commit using Conventional Commits
git commit -m "feat: add PDF upload support"

# 4. Push and open a Pull Request against main
git push origin feat/your-feature-name
```

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for full terms.

---

<div align="center">

**Built with 🧠 AI + ❤️ for the finance community**

*If this project saved you time, a ⭐ means everything.*

[![Star this repo](https://img.shields.io/github/stars/savera1226/financial-data-extractor?style=social)](https://github.com/savera1226/financial-data-extractor)

</div>
