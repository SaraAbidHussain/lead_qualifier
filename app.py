"""
Smart Lead Qualifier — Streamlit Frontend (Polished)
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from lead_qualifier.agent import qualify_lead, get_all_leads

st.set_page_config(
    page_title="LeadIQ — AI Lead Qualifier",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #080f1a; }
.main  { padding: 0 !important; }
section[data-testid="stSidebar"] { display: none; }

/* ── Layout shell ── */
.shell {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 2rem 4rem;
}

/* ── Top bar ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #1a2744;
}
.brand {
    display: flex;
    align-items: center;
    gap: 10px;
}
.brand-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #3b82f6, #6366f1);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}
.brand-name {
    font-size: 1.25rem;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: -0.02em;
}
.brand-tag {
    font-size: 0.7rem;
    color: #3b82f6;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-left: 4px;
    vertical-align: super;
}
.status-pill {
    background: #0d1f0d;
    border: 1px solid #166534;
    color: #4ade80;
    font-size: 0.75rem;
    font-weight: 500;
    padding: 4px 12px;
    border-radius: 20px;
    letter-spacing: 0.02em;
}

/* ── Two-column grid ── */
.grid {
    display: grid;
    grid-template-columns: 420px 1fr;
    gap: 1.5rem;
    align-items: start;
}

/* ── Panel ── */
.panel {
    background: #0d1625;
    border: 1px solid #1a2744;
    border-radius: 14px;
    padding: 1.5rem;
}
.panel-title {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 1.25rem;
}

/* ── Form fields ── */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background: #080f1a !important;
    border: 1px solid #1e3a5f !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    transition: border-color 0.2s !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
}
div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label {
    color: #64748b !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #2563eb !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.5rem !important;
    width: 100% !important;
    letter-spacing: 0.01em !important;
    transition: background 0.2s !important;
}
.stButton > button:hover { background: #1d4ed8 !important; }

/* ── Demo chips ── */
.demo-row {
    display: flex;
    gap: 8px;
    margin-bottom: 1.25rem;
    flex-wrap: wrap;
}
.demo-chip {
    background: #0d1625;
    border: 1px solid #1a2744;
    color: #94a3b8;
    font-size: 0.78rem;
    font-weight: 500;
    padding: 5px 14px;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.15s;
}
.demo-chip:hover { border-color: #3b82f6; color: #60a5fa; }

/* ── Score badge ── */
.score-block {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.score-badge {
    font-size: 0.95rem;
    font-weight: 700;
    padding: 8px 22px;
    border-radius: 24px;
    letter-spacing: 0.03em;
    white-space: nowrap;
}
.hot  { background: #3f0707; border: 1.5px solid #dc2626; color: #fca5a5; }
.warm { background: #3f1f07; border: 1.5px solid #ea580c; color: #fdba74; }
.cold { background: #07193f; border: 1.5px solid #2563eb; color: #93c5fd; }

.score-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #f1f5f9;
    line-height: 1;
}
.score-label {
    font-size: 0.72rem;
    color: #475569;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-top: 2px;
}

/* ── Section label ── */
.section-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #334155;
    margin: 1.25rem 0 0.6rem;
    padding-top: 1.25rem;
    border-top: 1px solid #0f1e35;
}

/* ── Reasoning text ── */
.reasoning {
    color: #94a3b8;
    font-size: 0.88rem;
    line-height: 1.65;
}

/* ── Needs pill ── */
.needs-text {
    background: #0d1f3c;
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 10px 14px;
    color: #7dd3fc;
    font-size: 0.88rem;
    line-height: 1.6;
}

/* ── Email box ── */
.email-wrap {
    background: #050d18;
    border: 1px solid #1a2744;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #cbd5e1;
    line-height: 1.75;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Progress pipeline ── */
.pipeline {
    display: flex;
    align-items: center;
    gap: 0;
    margin: 1rem 0 1.5rem;
    flex-wrap: wrap;
}
.pipe-step {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.78rem;
    color: #334155;
    padding: 5px 12px;
    border-radius: 20px;
    border: 1px solid #1a2744;
    background: #0a1628;
    margin: 3px;
    transition: all 0.3s;
}
.pipe-step.done {
    color: #4ade80;
    border-color: #166534;
    background: #0d1f0d;
}
.pipe-step.active {
    color: #60a5fa;
    border-color: #2563eb;
    background: #0d1f3c;
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.65; }
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: #1e3a5f;
}
.empty-icon { font-size: 3rem; margin-bottom: 1rem; opacity: 0.4; }
.empty-text { font-size: 0.9rem; color: #334155; line-height: 1.6; }

/* ── Metrics row ── */
.metrics {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.metric-card {
    background: #0d1625;
    border: 1px solid #1a2744;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.metric-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.75rem;
    font-weight: 700;
    color: #f1f5f9;
    line-height: 1;
}
.metric-lbl {
    font-size: 0.72rem;
    color: #475569;
    margin-top: 4px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ── History row ── */
.lead-row {
    background: #0d1625;
    border: 1px solid #1a2744;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}
.lead-name { font-weight: 600; color: #e2e8f0; font-size: 0.92rem; }
.lead-co   { color: #475569; font-size: 0.82rem; margin-top: 2px; }
.lead-date { color: #334155; font-size: 0.75rem; font-family: 'JetBrains Mono'; }

/* ── Streamlit tab overrides ── */
button[data-baseweb="tab"] {
    color: #475569 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #f1f5f9 !important;
}
</style>
""", unsafe_allow_html=True)

# ── DEMO DATA ──────────────────────────────────────────────
DEMOS = [
    {
        "label":   "🔥 Hot lead",
        "name":    "Ahmed Raza",
        "email":   "ahmed@techstartup.io",
        "company": "TechStartup.io",
        "message": "Hi — we're a 50-person SaaS company and urgently need an AI chatbot to handle customer support and qualify inbound leads automatically. Budget is around $5k and we want to move fast. Can we get on a call this week?"
    },
    {
        "label":   "🌡️ Warm lead",
        "name":    "Omar Sheikh",
        "email":   "omar@retailchain.com",
        "company": "Premier Retail",
        "message": "We have stores across Pakistan and are exploring AI for customer service. Not sure exactly what we need yet — could you walk me through what's possible?"
    },
    {
        "label":   "🧊 Cold lead",
        "name":    "Sara Khan",
        "email":   "sara@university.edu",
        "company": "University Lab",
        "message": "Hello, I'm a student researching AI chatbots for my thesis. Could you explain how your technology works? I'd love to learn more."
    },
]

# ── SESSION STATE ──────────────────────────────────────────
for key, val in {
    "result": None,
    "stages": [],
    "active_stage": None,
    "demo_data": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ══════════════════════════════════════════════════════════
# TOP BAR
# ══════════════════════════════════════════════════════════
st.markdown("""
<div class="shell">
<div class="topbar">
  <div class="brand">
    <div class="brand-icon">🎯</div>
    <span class="brand-name">LeadIQ<span class="brand-tag">AI</span></span>
  </div>
  <span class="status-pill">● Live</span>
</div>
</div>
""", unsafe_allow_html=True)

tab_qualify, tab_history = st.tabs(["Qualify Lead", "Lead History"])

# ══════════════════════════════════════════════════════════
# TAB 1 — QUALIFY
# ══════════════════════════════════════════════════════════
with tab_qualify:
    col_form, col_result = st.columns([5, 6], gap="large")

    # ── FORM ──────────────────────────────────────────────
    with col_form:
        st.markdown('<div class="panel-title">Lead details</div>', unsafe_allow_html=True)

        # Demo chips
        d_cols = st.columns(3)
        for i, (col, demo) in enumerate(zip(d_cols, DEMOS)):
            with col:
                if st.button(demo["label"], key=f"d{i}", use_container_width=True):
                    st.session_state.demo_data = demo
                    st.session_state.result = None
                    st.session_state.stages = []
                    st.rerun()

        st.markdown("<div style='margin-bottom:1rem'></div>", unsafe_allow_html=True)

        d = st.session_state.demo_data or {}
        name    = st.text_input("Name",    value=d.get("name",""),    placeholder="Ahmed Raza")
        email   = st.text_input("Email",   value=d.get("email",""),   placeholder="ahmed@company.com")
        company = st.text_input("Company", value=d.get("company",""), placeholder="Acme Corp")
        message = st.text_area("Message",  value=d.get("message",""), placeholder="What they wrote…", height=140)

        run_btn = st.button("Qualify →", use_container_width=True)

    # ── OUTPUT ────────────────────────────────────────────
    with col_result:
        st.markdown('<div class="panel-title">Analysis</div>', unsafe_allow_html=True)

        # Pipeline stages
        STAGES = [
            ("researching",    "🔍 Research"),
            ("analyzing",      "🧠 Analyze"),
            ("drafting_email", "✉️ Draft"),
            ("saving",         "💾 Save"),
        ]

        if run_btn:
            if not all([name, email, company, message]):
                st.error("Fill in all fields first.")
            else:
                st.session_state.result = None
                st.session_state.stages = []

                # Pipeline display
                pipeline_placeholder = st.empty()
                stages_done = []

                def render_pipeline(active=None):
                    html = '<div class="pipeline">'
                    for key, label in STAGES:
                        if key in stages_done:
                            cls = "done"
                        elif key == active:
                            cls = "active"
                        else:
                            cls = ""
                        html += f'<div class="pipe-step {cls}">{label}</div>'
                    html += "</div>"
                    pipeline_placeholder.markdown(html, unsafe_allow_html=True)

                render_pipeline()

                def on_progress(stage):
                    if stage not in stages_done:
                        stages_done.append(stage)
                    render_pipeline(active=stage)

                with st.spinner(""):
                    result = qualify_lead(
                        name=name, email=email,
                        company=company, message=message,
                        progress_callback=on_progress
                    )

                # Mark all done
                for key, _ in STAGES:
                    if key not in stages_done:
                        stages_done.append(key)
                render_pipeline()

                st.session_state.result = result
                st.session_state.stages = stages_done

        # ── RESULTS ───────────────────────────────────────
        if st.session_state.result:
            r     = st.session_state.result
            score = r.get("score", "Warm")

            badge_cls = {"Hot": "hot", "Warm": "warm", "Cold": "cold"}.get(score, "warm")
            emoji     = {"Hot": "🔥", "Warm": "🌡️", "Cold": "🧊"}.get(score, "🌡️")
            score_num = {"Hot": "82", "Warm": "51", "Cold": "23"}.get(score, "51")

            # Score row
            st.markdown(f"""
<div class="score-block">
  <div>
    <div class="score-num">{score_num}</div>
    <div class="score-label">Score / 100</div>
  </div>
  <span class="score-badge {badge_cls}">{emoji} {score} Lead</span>
</div>
<div class="reasoning">{r.get("score_reasoning","")}</div>
""", unsafe_allow_html=True)

            # What they need
            if r.get("needs_summary"):
                st.markdown('<div class="section-label">What they need</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="needs-text">{r["needs_summary"]}</div>', unsafe_allow_html=True)

            # Email draft
            if r.get("email_draft"):
                st.markdown('<div class="section-label">Draft reply</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="email-wrap">{r["email_draft"]}</div>', unsafe_allow_html=True)
                st.download_button(
                    "Download email draft",
                    data=r["email_draft"],
                    file_name=f"reply_{name.replace(' ','_').lower()}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            # Research (collapsed)
            if r.get("research_results") and r["research_results"] != "Research unavailable.":
                with st.expander("Company research", expanded=False):
                    st.markdown(
                        f'<div class="reasoning">{r["research_results"][:700]}</div>',
                        unsafe_allow_html=True
                    )

            if r.get("saved"):
                st.success("Saved to lead database.")

        elif not run_btn:
            st.markdown("""
<div class="empty-state">
  <div class="empty-icon">🎯</div>
  <div class="empty-text">
    Pick a demo lead above<br>or fill in the form and hit <strong>Qualify →</strong>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# TAB 2 — HISTORY
# ══════════════════════════════════════════════════════════
with tab_history:
    leads = get_all_leads()

    if not leads:
        st.markdown("""
<div class="empty-state">
  <div class="empty-icon">📊</div>
  <div class="empty-text">No leads yet. Qualify your first lead to see history.</div>
</div>
""", unsafe_allow_html=True)
    else:
        total = len(leads)
        hot   = sum(1 for l in leads if l.get("score") == "Hot")
        warm  = sum(1 for l in leads if l.get("score") == "Warm")
        cold  = sum(1 for l in leads if l.get("score") == "Cold")

        st.markdown(f"""
<div class="metrics">
  <div class="metric-card">
    <div class="metric-val">{total}</div>
    <div class="metric-lbl">Total</div>
  </div>
  <div class="metric-card">
    <div class="metric-val" style="color:#f87171">{hot}</div>
    <div class="metric-lbl">🔥 Hot</div>
  </div>
  <div class="metric-card">
    <div class="metric-val" style="color:#fb923c">{warm}</div>
    <div class="metric-lbl">🌡️ Warm</div>
  </div>
  <div class="metric-card">
    <div class="metric-val" style="color:#60a5fa">{cold}</div>
    <div class="metric-lbl">🧊 Cold</div>
  </div>
</div>
""", unsafe_allow_html=True)

        for lead in leads:
            score = lead.get("score", "?")
            emoji = {"Hot": "🔥", "Warm": "🌡️", "Cold": "🧊"}.get(score, "❓")
            badge_cls = {"Hot": "hot", "Warm": "warm", "Cold": "cold"}.get(score, "warm")

            with st.expander(
                f"{emoji}  {lead['name']}  ·  {lead['company']}  ·  {lead['timestamp'][:10]}",
                expanded=False
            ):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**Email:** {lead['email']}")
                    st.markdown(f"**Score:** {score}")
                    st.markdown(f"**Need:** {lead.get('needs','—')}")
                with c2:
                    st.markdown(f"**Reasoning:** {lead.get('reasoning','—')}")
                if lead.get("email_draft"):
                    st.markdown("**Draft reply:**")
                    st.markdown(
                        f'<div class="email-wrap">{lead["email_draft"]}</div>',
                        unsafe_allow_html=True
                    )

        # CSV export
        st.markdown("<br>", unsafe_allow_html=True)
        import csv, io
        out = io.StringIO()
        writer = csv.DictWriter(out, fieldnames=leads[0].keys())
        writer.writeheader()
        writer.writerows(leads)
        st.download_button(
            "Export all leads as CSV",
            data=out.getvalue(),
            file_name="leads_export.csv",
            mime="text/csv",
            use_container_width=False
        )