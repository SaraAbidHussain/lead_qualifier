# 🎯 LeadIQ — AI-Powered Lead Qualifier

> Stop wasting hours manually qualifying leads. LeadIQ researches, scores, and drafts replies for every inbound lead — in under 30 seconds.

**🔗 Live Demo:** [leadiq.streamlit.app](https://leadqualifier-2guv6kf8wunzpguatdmkxq.streamlit.app/) 

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![LangGraph](https://img.shields.io/badge/LangGraph-latest-green)
![Mistral](https://img.shields.io/badge/Mistral_AI-small--latest-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-deployed-red?logo=streamlit)

---

## The Problem It Solves

Sales teams receive dozens of inbound leads daily. Manually researching each company, deciding if they're worth pursuing, and writing a personalized reply takes 15–30 minutes per lead. Most leads never get a timely response.

**LeadIQ does this in 30 seconds.**

---

## What It Does

1. **Receives** a lead (name, email, company, message)
2. **Researches** the company automatically via web search
3. **Scores** the lead: 🔥 Hot / 🌡️ Warm / 🧊 Cold with reasoning
4. **Drafts** a personalized reply email
5. **Saves** everything to a local database with export to CSV

---

## Screenshots

| Lead Input + Scoring | Lead History |
|---|---|
| ![Qualify](screenshots/qualify.png) | ![History](screenshots/history.png) |

---

## Architecture

```
Lead Input (Streamlit)
        │
        ▼
┌─────────────────────────────────────────┐
│           LangGraph Pipeline            │
│                                         │
│  [Research] → [Analyze] → [Draft] → [Save] │
│                                         │
│  • DuckDuckGo web search                │
│  • Mistral AI for scoring + drafting    │
│  • SQLite for persistence               │
└─────────────────────────────────────────┘
        │
        ▼
  Results + Email Draft (Streamlit UI)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agent Framework | LangGraph (StateGraph + conditional edges) |
| LLM | Mistral AI `mistral-small-latest` |
| Web Search | DuckDuckGo (free, no API key) |
| Database | SQLite (zero config, built into Python) |
| Frontend | Streamlit |
| Deployment | Streamlit Cloud |

**100% free to run** — no paid APIs except Mistral (free tier available).

---

## Run Locally

```bash
git clone https://github.com/SaraAbidHussain/lead-qualifier
cd lead-qualifier
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `.env` file:
```
MISTRAL_API_KEY=your-key-here
```

Run:
```bash
streamlit run app.py
```

---

## Project Structure

```
lead-qualifier/
├── app.py                  # Streamlit frontend
├── lead_qualifier/
│   └── agent.py            # LangGraph pipeline
├── requirements.txt
├── .env                    # API key (never committed)
└── README.md
```

---

## Business Value

- **Saves 15–30 min per lead** on manual research and email writing
- **Consistent scoring** — no subjective gut-feel decisions
- **Instant response drafts** — reply to leads within minutes, not hours
- **Full audit trail** — every lead scored and stored with reasoning

---

Built by **Sara Abid** — CS Sophomore at ITU Lahore, building AI automation tools for businesses.

- 🐙 GitHub: [SaraAbidHussain](https://github.com/SaraAbidHussain)
- 💼 Available for freelance AI agent and automation projects