import html as _html
import re

import streamlit as st

from orchestrator import StartupAnalyzer

st.set_page_config(
    page_title="Startup Idea Analyzer",
    page_icon="📈",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

:root {
  --paper: #F5F6F3;
  --surface: #FFFFFF;
  --ink: #18211F;
  --muted: #58655F;
  --line: #DCE1DD;
  --pine: #1F4D45;
  --pine-dark: #173A34;
  --saffron: #D9981E;
  --good: #2E7D5B;
  --mid: #B7791A;
  --mid-text: #8A5A00;
  --low: #B54040;
}

html, body, .stApp, [data-testid="stApp"] {
  background: var(--paper) !important;
  color: var(--ink);
  font-family: 'IBM Plex Sans', system-ui, -apple-system, 'Segoe UI', sans-serif;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"], [data-testid="stDecoration"], #MainMenu, footer {
  display: none !important;
}
.block-container {
  max-width: 1100px;
  padding: 1.2rem 1.5rem 4rem;
}

h1, h2, h3, h4 {
  font-family: 'Bricolage Grotesque', 'IBM Plex Sans', sans-serif !important;
  color: var(--ink) !important;
  letter-spacing: -0.01em;
}
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
  color: var(--ink);
  line-height: 1.65;
  font-size: 0.98rem;
}

/* Top bar */
.topbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 0 18px; border-bottom: 1px solid var(--line);
}
.brand {
  display: flex; align-items: center; gap: 10px;
  font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700;
  font-size: 1.1rem; color: var(--ink);
}
.brand-mark {
  width: 22px; height: 22px; border-radius: 6px; background: var(--pine);
  position: relative; display: inline-block;
}
.brand-mark::after {
  content: ""; position: absolute; right: 4px; bottom: 4px;
  width: 7px; height: 7px; border-radius: 50%; background: var(--saffron);
}
.topbar-note { color: var(--muted); font-size: 0.9rem; }

/* Hero */
.hero { padding: 44px 0 10px; max-width: 760px; }
.hero h1 {
  font-size: clamp(2.1rem, 5vw, 3.3rem); line-height: 1.05;
  margin: 0 0 18px; font-weight: 700;
}
.hero p.lead {
  font-size: 1.12rem; line-height: 1.6; color: var(--muted) !important;
  margin: 0; max-width: 640px;
}
.steps {
  display: flex; flex-wrap: wrap; gap: 10px 28px; margin: 28px 0 8px;
  padding: 0; list-style: none;
}
.steps li {
  display: flex; align-items: center; gap: 10px;
  font-size: 0.93rem; color: var(--ink);
}
.steps .n {
  width: 24px; height: 24px; border-radius: 50%; flex: none;
  background: var(--pine); color: #fff; font-weight: 600; font-size: 0.8rem;
  display: inline-flex; align-items: center; justify-content: center;
}

/* Form */
[data-testid="stForm"] {
  background: var(--surface); border: 1px solid var(--line) !important;
  border-radius: 16px; padding: 28px 28px 24px;
}
.group-title {
  font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700;
  font-size: 1.15rem; color: var(--ink); margin: 0 0 2px;
}
[data-testid="stMarkdownContainer"] .group-sub { color: var(--muted); font-size: 0.9rem; margin: 0 0 14px; }

[data-testid="stWidgetLabel"] p, label p {
  color: var(--ink) !important; font-weight: 600; font-size: 0.92rem;
}
[data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] > div,
[data-testid="stTextInput"] div:has(> input),
[data-testid="stTextArea"] div:has(> textarea),
[data-testid="stSelectbox"] div:has(> input) {
  background: #fff !important; border: 1px solid #C9D0CC !important;
  border-radius: 10px !important;
}
[data-baseweb="input"]:focus-within,
[data-baseweb="textarea"]:focus-within,
[data-baseweb="select"] > div:focus-within,
[data-testid="stTextInput"] div:has(> input):focus-within,
[data-testid="stTextArea"] div:has(> textarea):focus-within,
[data-testid="stSelectbox"] div:has(> input):focus-within {
  border-color: var(--pine) !important;
  box-shadow: 0 0 0 3px rgba(31, 77, 69, 0.18) !important;
}
.stTextInput input, .stTextArea textarea {
  color: var(--ink) !important; -webkit-text-fill-color: var(--ink);
  background: transparent !important; font-size: 0.97rem;
  font-family: 'IBM Plex Sans', system-ui, sans-serif !important;
}
input::placeholder, textarea::placeholder {
  color: #85928C !important; -webkit-text-fill-color: #85928C; opacity: 1;
}
[data-baseweb="select"] * { color: var(--ink) !important; }
[data-baseweb="popover"] [role="listbox"], [data-baseweb="popover"] li,
[data-baseweb="menu"] {
  background: #fff !important; color: var(--ink) !important;
}

/* Buttons */
.stButton > button, .stDownloadButton > button,
[data-testid="stFormSubmitButton"] > button {
  border-radius: 10px; font-weight: 600; min-height: 46px;
  border: 1px solid #C9D0CC; background: #fff; color: var(--ink);
  font-family: 'IBM Plex Sans', sans-serif;
}
.stButton > button:hover, .stDownloadButton > button:hover {
  border-color: var(--pine); color: var(--pine);
}
[data-testid="stFormSubmitButton"] > button,
.stButton > button[kind="primary"] {
  background: var(--pine) !important; border-color: var(--pine) !important;
  color: #fff !important; min-height: 50px; font-size: 1rem;
}
[data-testid="stFormSubmitButton"] > button p { color: #fff !important; }
[data-testid="stFormSubmitButton"] > button:hover {
  background: var(--pine-dark) !important; border-color: var(--pine-dark) !important;
}
button:focus-visible {
  outline: 3px solid rgba(217, 152, 30, 0.6) !important; outline-offset: 2px;
}

/* Progress */
.progress-card {
  background: var(--surface); border: 1px solid var(--line);
  border-radius: 14px; padding: 22px 24px; margin-top: 18px;
}
.progress-top { display: flex; justify-content: space-between; gap: 12px; }
.progress-msg { font-weight: 600; color: var(--ink); }
.progress-pct { color: var(--muted); font-variant-numeric: tabular-nums; }
.bar { height: 8px; background: #E6EAE7; border-radius: 99px; margin: 14px 0 10px; overflow: hidden; }
.bar > span { display: block; height: 100%; background: var(--pine); border-radius: 99px; transition: width .4s ease; }
.progress-note { color: var(--muted); font-size: 0.88rem; margin: 0; }

/* Callouts */
.callout {
  border-radius: 12px; padding: 16px 18px; margin: 16px 0;
  border: 1px solid var(--line); background: var(--surface);
  border-left: 5px solid var(--low);
}
.callout.info { border-left-color: var(--pine); }
.callout .c-title { font-weight: 600; color: var(--ink); margin: 0 0 4px; }
.callout p { margin: 0; color: var(--muted) !important; font-size: 0.93rem; }
.callout .c-detail { margin-top: 8px !important; font-size: 0.8rem !important; word-break: break-word; }

/* Results */
.result-head { margin: 36px 0 4px; }
.result-head h2 { font-size: 1.7rem; margin: 0 0 4px; font-weight: 700; }
.result-head p { color: var(--muted) !important; margin: 0; }

.ov-grid {
  display: grid; grid-template-columns: 320px 1fr; gap: 20px; margin: 18px 0 20px;
}
@media (max-width: 860px) { .ov-grid { grid-template-columns: 1fr; } }

.card {
  background: var(--surface); border: 1px solid var(--line);
  border-radius: 14px; padding: 24px;
}
.gauge-card { display: flex; flex-direction: column; align-items: center; text-align: center; }
.gauge {
  width: 190px; height: 190px; border-radius: 50%;
  background: conic-gradient(var(--c) calc(var(--pct) * 1%), #E6EAE7 0);
  display: flex; align-items: center; justify-content: center;
}
.gauge-inner {
  width: 148px; height: 148px; border-radius: 50%; background: var(--surface);
  display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.gauge-num {
  font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700;
  font-size: 3.1rem; line-height: 1; color: var(--ink);
}
.gauge-den { color: var(--muted); font-size: 0.9rem; margin-top: 2px; }
.verdict { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700; font-size: 1.25rem; margin: 16px 0 4px; }
.verdict.good { color: var(--good); } .verdict.mid { color: var(--mid-text); } .verdict.low { color: var(--low); }
.gauge-card p.fine { color: var(--muted) !important; font-size: 0.85rem; line-height: 1.5; margin: 6px 0 0; }
.chip {
  display: inline-block; padding: 4px 12px; border-radius: 99px; font-size: 0.82rem;
  font-weight: 600; background: #EDF1EE; color: var(--ink); margin-top: 12px;
}

.next-panel {
  background: var(--pine); border-radius: 14px; padding: 28px;
  display: flex; flex-direction: column; justify-content: center;
}
.next-panel, .next-panel * { color: #fff !important; }
.next-panel .n-label { font-weight: 600; font-size: 0.95rem; opacity: .85; margin: 0 0 8px; }
.next-panel .n-text {
  font-family: 'Bricolage Grotesque', sans-serif; font-weight: 500;
  font-size: 1.45rem; line-height: 1.35; margin: 0;
}
.next-panel .n-focus { margin: 20px 0 0; padding-top: 16px; border-top: 1px solid rgba(255,255,255,.25); font-size: .93rem; line-height: 1.55; opacity: .92; }
.next-panel .n-focus b { font-weight: 600; }

.finding {
  background: var(--surface); border: 1px solid var(--line);
  border-left: 5px solid var(--c); border-radius: 12px; padding: 16px 20px; margin-bottom: 12px;
}
.finding .f-tag { font-weight: 600; color: var(--c-text); font-size: 0.92rem; margin: 0 0 4px; }
.finding p.f-body { margin: 0; color: var(--ink) !important; line-height: 1.6; }
.f-good { --c: var(--good); --c-text: var(--good); }
.f-low { --c: var(--low); --c-text: var(--low); }
.f-mid { --c: var(--mid); --c-text: var(--mid-text); }

.section-title {
  font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700;
  font-size: 1.2rem; margin: 26px 0 12px; color: var(--ink);
}
.cat-row {
  display: grid; grid-template-columns: 210px 1fr 64px; gap: 14px; align-items: center;
  padding: 9px 0; border-bottom: 1px solid #EEF1EF;
}
.cat-row:last-child { border-bottom: none; }
.cat-name { font-size: 0.95rem; color: var(--ink); }
.cat-bar { height: 10px; border-radius: 99px; background: #E6EAE7; overflow: hidden; }
.cat-bar > span { display: block; height: 100%; border-radius: 99px; background: var(--c); }
.cat-val { text-align: right; font-weight: 600; font-variant-numeric: tabular-nums; color: var(--ink); }
.cat-row.good { --c: var(--good); } .cat-row.mid { --c: var(--mid); } .cat-row.low { --c: var(--low); }
@media (max-width: 640px) { .cat-row { grid-template-columns: 1fr 56px; } .cat-bar { grid-column: 1 / -1; order: 3; } }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 6px; border-bottom: 1px solid var(--line); flex-wrap: wrap; }
.stTabs [data-baseweb="tab"] { padding: 10px 14px; background: transparent; }
.stTabs [data-baseweb="tab"] p { color: var(--muted) !important; font-weight: 600; font-size: 0.95rem; }
.stTabs [aria-selected="true"] p { color: var(--pine) !important; }
.stTabs [data-baseweb="tab-highlight"] { background: var(--pine) !important; height: 3px; }
.stTabs [data-baseweb="tab-border"] { display: none; }

/* Expanders */
[data-testid="stExpander"] {
  background: var(--surface); border: 1px solid var(--line) !important;
  border-radius: 12px !important; margin-bottom: 10px; overflow: hidden;
}
[data-testid="stExpander"] details, [data-testid="stExpander"] summary {
  background: var(--surface) !important;
}
[data-testid="stExpander"] summary p, [data-testid="stExpander"] summary span {
  color: var(--ink) !important; font-weight: 600;
}

/* Lists and items */
.pill {
  display: inline-block; padding: 2px 10px; border-radius: 99px; font-size: .8rem;
  font-weight: 600; background: #EDF1EE; color: var(--ink); margin-right: 6px;
}
.pill.high { background: #F6E3E3; color: var(--low); }
.pill.medium { background: #FBF0D9; color: var(--mid-text); }
.pill.low { background: #E1F0E8; color: var(--good); }
ul.plain { margin: 6px 0 14px; padding-left: 20px; }
ul.plain li { margin: 4px 0; color: var(--ink); line-height: 1.6; }
.mini-title { font-weight: 600; color: var(--ink); margin: 14px 0 2px; font-size: .92rem; }
.item {
  background: var(--surface); border: 1px solid var(--line); border-left: 5px solid var(--low);
  border-radius: 12px; padding: 14px 18px; margin-bottom: 10px; color: var(--ink); line-height: 1.6;
}
.item.warn { border-left-color: var(--mid); }
.exp {
  background: var(--surface); border: 1px solid var(--line); border-radius: 12px;
  padding: 18px 20px; margin-bottom: 12px;
}
.exp .e-title { font-weight: 600; color: var(--ink); margin: 0 0 8px; line-height: 1.5; }
.exp .e-row { margin: 4px 0 0; color: var(--ink); line-height: 1.6; font-size: .95rem; }
.exp .e-row b { font-weight: 600; }

.timeline { position: relative; margin: 8px 0 0; padding-left: 0; list-style: none; }
.timeline li { position: relative; padding: 0 0 18px 52px; min-height: 36px; color: var(--ink); line-height: 1.6; }
.timeline li::before {
  content: ""; position: absolute; left: 15px; top: 34px; bottom: 0; width: 2px; background: var(--line);
}
.timeline li:last-child::before { display: none; }
.timeline .d {
  position: absolute; left: 0; top: 0; width: 32px; height: 32px; border-radius: 50%;
  background: var(--pine); color: #fff; font-weight: 600; font-size: .9rem;
  display: flex; align-items: center; justify-content: center;
}
.timeline .d-label { display: block; font-weight: 600; font-size: .85rem; color: var(--muted); }

.agent-score { color: var(--muted); font-size: .9rem; margin: 0 0 8px; }
.note { color: var(--muted) !important; font-size: .9rem; margin: 4px 0 14px; }
.disclaimer { color: var(--muted) !important; font-size: .85rem; margin-top: 36px; padding-top: 16px; border-top: 1px solid var(--line); }
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def H(markup: str) -> str:
    """Collapse HTML to a single line so Markdown never treats it as code."""
    return " ".join(line.strip() for line in markup.splitlines() if line.strip())


def esc(value) -> str:
    return _html.escape(" ".join(str(value).split()))


def safe_md(text) -> str:
    """Stop dollar signs from being rendered as math."""
    return str(text).replace("$", "\\$")


def band(score: int):
    if score >= 70:
        return "good", "Strong case so far"
    if score >= 50:
        return "mid", "Promising, needs proof"
    return "low", "Weak case today"


def bullets(items) -> str:
    return "<ul class='plain'>" + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"


def callout(title: str, body: str = "", kind: str = "error", detail: str = ""):
    detail_html = f"<p class='c-detail'>{esc(detail)}</p>" if detail else ""
    body_html = f"<p>{esc(body)}</p>" if body else ""
    st.markdown(
        H(
            f"<div class='callout {kind}'><p class='c-title'>{esc(title)}</p>"
            f"{body_html}{detail_html}</div>"
        ),
        unsafe_allow_html=True,
    )


def render_progress(slot, message: str, pct: int):
    pct = max(0, min(100, int(pct)))
    slot.markdown(
        H(
            f"""
            <div class='progress-card'>
              <div class='progress-top'>
                <span class='progress-msg'>{esc(message)}</span>
                <span class='progress-pct'>{pct}%</span>
              </div>
              <div class='bar'><span style='width:{pct}%'></span></div>
              <p class='progress-note'>This takes a few minutes. Keep this tab open until it finishes.</p>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )


EXAMPLE = {
    "f_name": "FarmDirect",
    "f_idea": (
        "A WhatsApp bot and app that connects small farmers directly with "
        "grocery shops and restaurants, so they can sell produce without middlemen."
    ),
    "f_problem": (
        "Small farmers lose 30-40% of their profit to commission agents and "
        "have no price transparency."
    ),
    "f_customer": (
        "Farmers with 5-25 acres in southern Punjab, plus grocery stores and "
        "restaurants in Rahim Yar Khan, Bahawalpur and Multan."
    ),
    "f_solution": (
        "Farmers post daily produce and prices, buyers order in the app, and we "
        "arrange transport and payment through JazzCash or Easypaisa."
    ),
    "f_model": "5% commission per order",
    "f_location": "Pakistan",
    "f_industry": "AgriTech",
    "f_stage": "MVP",
}


def load_example():
    for key, value in EXAMPLE.items():
        st.session_state[key] = value


# ---------------------------------------------------------------------------
# Header and hero
# ---------------------------------------------------------------------------

st.markdown(
    H(
        """
        <div class='topbar'>
          <div class='brand'><span class='brand-mark'></span>Startup Idea Analyzer</div>
          <div class='topbar-note'>Validate before you build</div>
        </div>
        <div class='hero'>
          <h1>Know what to test before you build.</h1>
          <p class='lead'>Describe your startup idea. Eleven AI agents review the problem,
          customer, market, competitors, business model and risks. A red team then
          challenges the result and you get a 7-day plan to test it.</p>
          <ol class='steps'>
            <li><span class='n'>1</span>Describe your idea</li>
            <li><span class='n'>2</span>Agents research and score it</li>
            <li><span class='n'>3</span>A red team challenges it</li>
            <li><span class='n'>4</span>Get your 7-day test plan</li>
          </ol>
        </div>
        """
    ),
    unsafe_allow_html=True,
)

_, example_col = st.columns([4, 1])
with example_col:
    st.button("Fill with an example", on_click=load_example, use_container_width=True)

# ---------------------------------------------------------------------------
# Input form
# ---------------------------------------------------------------------------

with st.form("startup_form"):
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            "<p class='group-title'>The idea</p>"
            "<p class='group-sub'>What you are building and why.</p>",
            unsafe_allow_html=True,
        )
        startup_name = st.text_input(
            "Startup Name", placeholder="e.g. StudyPilot", key="f_name"
        )
        idea = st.text_area(
            "What are you building?",
            placeholder="Describe the product or service.",
            height=120,
            key="f_idea",
        )
        problem = st.text_area(
            "What problem are you solving?",
            placeholder="Describe the customer problem.",
            height=100,
            key="f_problem",
        )
        solution = st.text_area(
            "What is your proposed solution?",
            placeholder="Explain how your product solves the problem.",
            height=100,
            key="f_solution",
        )

    with col2:
        st.markdown(
            "<p class='group-title'>The market</p>"
            "<p class='group-sub'>Who it is for and how it earns.</p>",
            unsafe_allow_html=True,
        )
        customer = st.text_area(
            "Who is your customer?",
            placeholder="Be as specific as possible.",
            height=120,
            key="f_customer",
        )
        business_model = st.text_input(
            "How will you make money?",
            placeholder="e.g. subscription, freemium, commission",
            key="f_model",
        )
        location = st.text_input(
            "Where will you launch?",
            placeholder="e.g. Pakistan",
            key="f_location",
        )
        industry = st.text_input(
            "Industry",
            placeholder="e.g. EdTech",
            key="f_industry",
        )
        stage = st.selectbox(
            "Current Stage",
            ["Idea", "Prototype", "MVP", "Early Revenue", "Growth"],
            key="f_stage",
        )

    submitted = st.form_submit_button(
        "Analyze idea",
        type="primary",
        use_container_width=True,
    )

progress_slot = st.empty()

# ---------------------------------------------------------------------------
# Run analysis
# ---------------------------------------------------------------------------

if submitted:
    missing = []
    for label, value in [
        ("Startup Name", startup_name),
        ("Idea", idea),
        ("Problem", problem),
        ("Customer", customer),
        ("Solution", solution),
        ("Location", location),
        ("Industry", industry),
    ]:
        if not value.strip():
            missing.append(label)

    if missing:
        callout(
            "Some fields are empty",
            "Fill in these fields and analyze again: " + ", ".join(missing) + ".",
        )
        st.stop()

    startup = {
        "startup_name": startup_name.strip(),
        "idea": idea.strip(),
        "problem": problem.strip(),
        "customer": customer.strip(),
        "solution": solution.strip(),
        "business_model": business_model.strip() or "Not specified",
        "location": location.strip(),
        "industry": industry.strip(),
        "stage": stage,
    }

    st.session_state.pop("result", None)
    analyzer = StartupAnalyzer()
    render_progress(progress_slot, "Starting analysis", 0)

    try:
        result = analyzer.run(
            startup=startup,
            status_callback=lambda message, pct: render_progress(
                progress_slot, message, pct
            ),
        )
    except Exception as exc:
        progress_slot.empty()
        error_text = str(exc)
        if "429" in error_text or "rate_limit" in error_text.lower():
            callout(
                "Groq token limit reached",
                "Try again later, switch models in config.py, or upgrade your "
                "Groq plan.",
                detail=error_text,
            )
        elif "GROQ_API_KEY" in error_text or "401" in error_text:
            callout(
                "Groq API key problem",
                "Check that GROQ_API_KEY is set in Streamlit Cloud Secrets, "
                "then redeploy the app.",
                detail=error_text,
            )
        else:
            callout(
                "The analysis could not finish",
                "Run it again. If it keeps failing, the details below help "
                "find the cause.",
                detail=error_text,
            )
        st.stop()

    progress_slot.empty()
    st.session_state["result"] = result
    st.session_state["startup"] = startup

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------

result = st.session_state.get("result")

if result:
    startup = st.session_state.get("startup", {})
    report = result["report"]
    scores = result["scores"]
    overall = int(scores["overall"])
    tone, verdict = band(overall)
    name = startup.get("startup_name", "Your startup")

    st.markdown(
        H(
            f"""
            <div class='result-head'>
              <h2>{esc(name)}</h2>
              <p>{esc(startup.get('industry', ''))}, {esc(startup.get('location', ''))}, stage: {esc(startup.get('stage', ''))}</p>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    tab_overview, tab_agents, tab_research, tab_red, tab_plan, tab_report = st.tabs(
        [
            "Overview",
            "Agent analysis",
            "Research",
            "Red team",
            "Validation plan",
            "Full report",
        ]
    )

    # ---- Overview ----
    with tab_overview:
        st.markdown(
            H(
                f"""
                <div class='ov-grid'>
                  <div class='card gauge-card'>
                    <div class='gauge' style='--pct:{overall}; --c:var(--{tone});'>
                      <div class='gauge-inner'>
                        <span class='gauge-num'>{overall}</span>
                        <span class='gauge-den'>out of 100</span>
                      </div>
                    </div>
                    <div class='verdict {tone}'>{esc(verdict)}</div>
                    <p class='fine'>Validation readiness. This shows how strong the case looks on the information given. It is not a chance of success.</p>
                    <span class='chip'>Evidence strength: {esc(report['evidence_strength'])}</span>
                  </div>
                  <div class='next-panel'>
                    <p class='n-label'>Do this first</p>
                    <p class='n-text'>{esc(report['next_action'])}</p>
                    <p class='n-focus'><b>Decision focus:</b> {esc(report['decision_focus'])}</p>
                  </div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

        st.markdown(
            H(
                f"""
                <div class='finding f-good'><p class='f-tag'>Biggest strength</p><p class='f-body'>{esc(report['biggest_strength'])}</p></div>
                <div class='finding f-low'><p class='f-tag'>Biggest risk</p><p class='f-body'>{esc(report['biggest_risk'])}</p></div>
                <div class='finding f-mid'><p class='f-tag'>Biggest unknown</p><p class='f-body'>{esc(report['biggest_unknown'])}</p></div>
                """
            ),
            unsafe_allow_html=True,
        )

        rows = ""
        for cat_name, value in scores["categories"].items():
            value = int(value)
            cat_tone, _ = band(value)
            rows += (
                f"<div class='cat-row {cat_tone}'>"
                f"<span class='cat-name'>{esc(cat_name)}</span>"
                f"<span class='cat-bar'><span style='width:{max(0, min(100, value))}%'></span></span>"
                f"<span class='cat-val'>{value}/100</span></div>"
            )
        st.markdown(
            H(
                "<p class='section-title'>Category assessments</p>"
                f"<div class='card'>{rows}</div>"
            ),
            unsafe_allow_html=True,
        )

    # ---- Agent analysis ----
    with tab_agents:
        st.markdown(
            "<p class='note'>What each specialist agent concluded. Open an agent to see its evidence and open questions.</p>",
            unsafe_allow_html=True,
        )
        for item in result["agent_results"]:
            with st.expander(f"{item['agent']} agent: {item['score']}/100"):
                st.markdown(
                    H(
                        f"<p class='agent-score'><span class='pill'>Confidence: {esc(item['confidence'])}</span></p>"
                        f"<p>{esc(item['summary'])}</p>"
                    ),
                    unsafe_allow_html=True,
                )
                if item.get("evidence"):
                    st.markdown(
                        H("<p class='mini-title'>Evidence</p>" + bullets(item["evidence"])),
                        unsafe_allow_html=True,
                    )
                if item.get("unknowns"):
                    st.markdown(
                        H("<p class='mini-title'>Unknowns</p>" + bullets(item["unknowns"])),
                        unsafe_allow_html=True,
                    )

    # ---- Research ----
    with tab_research:
        st.markdown(
            "<p class='note'>Background the agents used. Check any figure here before you rely on it.</p>",
            unsafe_allow_html=True,
        )
        if result["research"]:
            st.markdown(safe_md(result["research"]))
        else:
            callout("No research was returned", kind="info")

    # ---- Red team ----
    with tab_red:
        red = result["red_team"]
        st.markdown("<p class='section-title'>Challenges</p>", unsafe_allow_html=True)
        for finding in red["challenges"]:
            st.markdown(
                f"<div class='item'>{esc(finding)}</div>", unsafe_allow_html=True
            )

        st.markdown(
            "<p class='section-title'>Critical assumptions questioned</p>",
            unsafe_allow_html=True,
        )
        for assumption in red["critical_assumptions"]:
            st.markdown(
                f"<div class='item warn'>{esc(assumption)}</div>",
                unsafe_allow_html=True,
            )

        if red.get("failure_modes"):
            st.markdown(
                "<p class='section-title'>How this could fail</p>",
                unsafe_allow_html=True,
            )
            for mode in red["failure_modes"]:
                st.markdown(
                    f"<div class='item'>{esc(mode)}</div>", unsafe_allow_html=True
                )

    # ---- Validation plan ----
    with tab_plan:
        st.markdown("<p class='section-title'>Experiments</p>", unsafe_allow_html=True)
        for item in result["validation"]["experiments"]:
            priority = str(item["priority"]).strip()
            pclass = priority.lower() if priority.lower() in ("high", "medium", "low") else ""
            st.markdown(
                H(
                    f"""
                    <div class='exp'>
                      <p class='e-title'>{esc(item['assumption'])}</p>
                      <p class='e-row'><b>Experiment:</b> {esc(item['experiment'])}</p>
                      <p class='e-row'><b>Success criterion:</b> {esc(item['success_criterion'])}</p>
                      <p class='e-row'><span class='pill {pclass}'>Priority: {esc(priority)}</span></p>
                    </div>
                    """
                ),
                unsafe_allow_html=True,
            )

        st.markdown(
            "<p class='section-title'>7-day validation roadmap</p>",
            unsafe_allow_html=True,
        )
        days = "".join(
            f"<li><span class='d'>{esc(day['day'])}</span>"
            f"<span class='d-label'>Day {esc(day['day'])}</span>{esc(day['action'])}</li>"
            for day in result["validation"]["seven_day_plan"]
        )
        st.markdown(H(f"<ul class='timeline'>{days}</ul>"), unsafe_allow_html=True)

    # ---- Full report ----
    with tab_report:
        sections = [
            ("Executive Summary", report["executive_summary"]),
            ("Problem Analysis", report["problem_analysis"]),
            ("Customer Analysis", report["customer_analysis"]),
            ("Market Analysis", report["market_analysis"]),
            ("Competitor Landscape", report["competitor_landscape"]),
            ("Differentiation", report["differentiation"]),
            ("Business Model", report["business_model"]),
            ("Technical & Operational Feasibility", report["feasibility"]),
            ("Risk Analysis", report["risk_analysis"]),
            ("Assumption Map", report["assumption_map"]),
            ("Red-Team Findings", report["red_team_findings"]),
            ("Validation Experiments", report["validation_experiments"]),
            ("7-Day Plan", report["seven_day_plan"]),
            ("Recommendations", report["recommendations"]),
        ]

        for title, content in sections:
            with st.expander(title, expanded=(title == "Executive Summary")):
                st.markdown(safe_md(content))

        markdown_report = (
            f"# {name}: validation report\n\n"
            f"Validation readiness: {overall}/100 ({verdict})\n\n"
            f"Evidence strength: {report['evidence_strength']}\n\n"
            f"Next action: {report['next_action']}\n\n"
            f"Decision focus: {report['decision_focus']}\n\n"
            + "\n\n".join(f"## {title}\n\n{content}" for title, content in sections)
        )
        file_slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "startup"

        st.download_button(
            "Download report (.md)",
            data=markdown_report,
            file_name=f"{file_slug}-validation-report.md",
            mime="text/markdown",
        )

    st.markdown(
        "<p class='disclaimer'>This report is AI-generated from the information you entered. "
        "Use the scores to decide what to test next, and check key facts yourself before you "
        "commit time or money.</p>",
        unsafe_allow_html=True,
    )
