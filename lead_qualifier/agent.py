"""
Smart Lead Qualifier Agent
Core LangGraph pipeline — no paid APIs required
"""

from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langchain_mistralai import ChatMistralAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
import sqlite3
import json
import os
from datetime import datetime

load_dotenv()

# ── CONFIG ─────────────────────────────────────────────────
DB_PATH = "/tmp/leads.db"
llm = ChatMistralAI(model="mistral-small-latest", temperature=0)

# ── STATE ──────────────────────────────────────────────────
class LeadState(TypedDict):
    name:             str
    email:            str
    company:          str
    message:          str
    research_results: str
    score:            str
    score_reasoning:  str
    needs_summary:    str
    email_draft:      str
    saved:            bool
    error_log:        list[str]
    current_stage:    str

# ── DATABASE SETUP ─────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT,
            name        TEXT,
            email       TEXT,
            company     TEXT,
            message     TEXT,
            research    TEXT,
            score       TEXT,
            reasoning   TEXT,
            needs       TEXT,
            email_draft TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ── NODE 1: Web Research ───────────────────────────────────
def web_research_node(state: LeadState) -> dict:
    updates = {"current_stage": "researching"}
    try:
        company = state["company"]
        queries = [
            f"{company} company what do they do",
            f"{company} company size industry",
        ]
        results = []
        for query in queries:
            try:
                result = search.invoke(query)
                results.append(result[:400])
            except Exception:
                pass

        research = "\n\n".join(results) if results else "No research data found."
        updates["research_results"] = research[:1200]

    except Exception as e:
        updates["research_results"] = "Research unavailable."
        updates["error_log"] = state.get("error_log", []) + [f"Research error: {str(e)}"]

    return updates

# ── NODE 2: Lead Analyzer ──────────────────────────────────
def lead_analyzer_node(state: LeadState) -> dict:
    updates = {"current_stage": "analyzing"}

    prompt = ChatPromptTemplate.from_template("""
You are an expert B2B sales analyst. Analyze this lead and return ONLY valid JSON.

Lead Information:
- Name: {name}
- Company: {company}
- Email: {email}
- Message: {message}

Company Research:
{research}

Scoring criteria:
- HOT: Clear need, decision-maker, specific request, good company fit
- WARM: Some interest shown, needs clarification, potential fit
- COLD: Vague inquiry, student/researcher, no budget signals, poor fit

Return this exact JSON structure:
{{
    "score": "Hot",
    "reasoning": "2-3 sentence explanation of score",
    "needs_summary": "What they specifically need in 1-2 sentences",
    "budget_signals": "Any budget or urgency indicators mentioned",
    "recommended_action": "Specific next step for sales team"
}}
""")

    try:
        chain = prompt | llm
        response = chain.invoke({
            "name":     state["name"],
            "company":  state["company"],
            "email":    state["email"],
            "message":  state["message"],
            "research": state.get("research_results", "Not available")
        })

        content = response.content.strip()
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        content = content.strip()

        data = json.loads(content)
        updates["score"]           = data.get("score", "Warm")
        updates["score_reasoning"] = data.get("reasoning", "")
        updates["needs_summary"]   = data.get("needs_summary", "")

    except Exception as e:
        updates["score"]           = "Warm"
        updates["score_reasoning"] = "Could not analyze — manual review needed."
        updates["needs_summary"]   = state["message"][:200]
        updates["error_log"]       = state.get("error_log", []) + [f"Analysis error: {str(e)}"]

    return updates

# ── NODE 3: Email Drafter ──────────────────────────────────
def email_drafter_node(state: LeadState) -> dict:
    updates = {"current_stage": "drafting_email"}

    prompt = ChatPromptTemplate.from_template("""
Write a professional reply email to this lead.

Lead: {name} from {company}
Their need: {needs}
Lead score: {score}

Tone guidelines:
- Hot lead: Enthusiastic, suggest a call this week, be specific
- Warm lead: Friendly, ask clarifying questions, provide value
- Cold lead: Professional, educational, low-pressure

Write ONLY the email body (no subject line needed).
Start with "Hi {name}," and end with a clear call to action.
Keep it under 150 words. Sound human, not templated.
""")

    try:
        chain = prompt | llm
        response = chain.invoke({
            "name":    state["name"],
            "company": state["company"],
            "needs":   state.get("needs_summary", state["message"]),
            "score":   state.get("score", "Warm")
        })
        updates["email_draft"] = response.content.strip()

    except Exception as e:
        updates["email_draft"] = f"Hi {state['name']},\n\nThank you for reaching out. We will be in touch shortly.\n\nBest regards"
        updates["error_log"]   = state.get("error_log", []) + [f"Email error: {str(e)}"]

    return updates

# ── NODE 4: Data Saver ─────────────────────────────────────
def data_saver_node(state: LeadState) -> dict:
    updates = {"current_stage": "saving"}

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("""
            INSERT INTO leads
            (timestamp, name, email, company, message,
             research, score, reasoning, needs, email_draft)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            state["name"],
            state["email"],
            state["company"],
            state["message"],
            state.get("research_results", ""),
            state.get("score", ""),
            state.get("score_reasoning", ""),
            state.get("needs_summary", ""),
            state.get("email_draft", "")
        ))
        conn.commit()
        conn.close()
        updates["saved"] = True

    except Exception as e:
        updates["saved"]     = False
        updates["error_log"] = state.get("error_log", []) + [f"Save error: {str(e)}"]

    updates["current_stage"] = "complete"
    return updates

# ── ROUTING ────────────────────────────────────────────────
def research_done(state: LeadState) -> str:
    return "analyze"

# ── BUILD GRAPH ────────────────────────────────────────────
def build_graph():
    graph_builder = StateGraph(LeadState)

    graph_builder.add_node("research",    web_research_node)
    graph_builder.add_node("analyze",     lead_analyzer_node)
    graph_builder.add_node("draft_email", email_drafter_node)
    graph_builder.add_node("save",        data_saver_node)

    graph_builder.add_edge(START, "research")
    graph_builder.add_conditional_edges(
        "research",
        research_done,
        {"analyze": "analyze"}
    )
    graph_builder.add_edge("analyze",     "draft_email")
    graph_builder.add_edge("draft_email", "save")
    graph_builder.add_edge("save",        END)

    return graph_builder.compile()

graph = build_graph()

# ── PUBLIC INTERFACE ───────────────────────────────────────
def qualify_lead(
    name: str,
    email: str,
    company: str,
    message: str,
    progress_callback=None
) -> LeadState:
    initial_state: LeadState = {
        "name":             name,
        "email":            email,
        "company":          company,
        "message":          message,
        "research_results": "",
        "score":            "",
        "score_reasoning":  "",
        "needs_summary":    "",
        "email_draft":      "",
        "saved":            False,
        "error_log":        [],
        "current_stage":    "starting"
    }

    final_state = None

    for update in graph.stream(initial_state, stream_mode="updates"):
        for node_name, node_state in update.items():
            if progress_callback:
                stage = node_state.get("current_stage", node_name)
                progress_callback(stage)
            final_state = node_state

    result = {**initial_state, **final_state} if final_state else initial_state
    return result


def get_all_leads() -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM leads ORDER BY timestamp DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]