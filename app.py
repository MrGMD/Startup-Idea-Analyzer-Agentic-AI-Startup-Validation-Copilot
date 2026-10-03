import streamlit as st
from orchestrator import StartupAnalyzer

st.set_page_config(
    page_title="Startup Idea Analyzer",
    page_icon="🚀",
    layout="wide",
)

st.title("🚀 Startup Idea Analyzer")
st.caption("Validate Before You Build.")

st.markdown(
    "Research your startup idea, challenge its assumptions, and get a practical "
    "validation plan before investing heavily in development."
)

with st.form("startup_form"):
    col1, col2 = st.columns(2)

    with col1:
        startup_name = st.text_input("Startup Name", placeholder="e.g. StudyPilot")
        idea = st.text_area(
            "What are you building?",
            placeholder="Describe the product or service.",
            height=120,
        )
        problem = st.text_area(
            "What problem are you solving?",
            placeholder="Describe the customer problem.",
            height=100,
        )
        customer = st.text_area(
            "Who is your customer?",
            placeholder="Be as specific as possible.",
            height=100,
        )

    with col2:
        solution = st.text_area(
            "What is your proposed solution?",
            placeholder="Explain how your product solves the problem.",
            height=120,
        )
        business_model = st.text_input(
            "How will you make money?",
            placeholder="e.g. subscription, freemium, commission",
        )
        location = st.text_input(
            "Where will you launch?",
            placeholder="e.g. Pakistan",
        )
        industry = st.text_input(
            "Industry",
            placeholder="e.g. EdTech",
        )
        stage = st.selectbox(
            "Current Stage",
            ["Idea", "Prototype", "MVP", "Early Revenue", "Growth"],
        )

    submitted = st.form_submit_button(
        "🔍 Analyze My Idea",
        type="primary",
        use_container_width=True,
    )

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
        st.error("Please complete: " + ", ".join(missing))
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

    analyzer = StartupAnalyzer()

    progress = st.progress(0)
    status = st.empty()

    try:
        result = analyzer.run(
            startup=startup,
            status_callback=lambda message, pct: (
                status.info(message),
                progress.progress(pct),
            ),
        )
    except Exception as exc:
        progress.empty()
        status.empty()
        error_text = str(exc)
        if "429" in error_text or "rate_limit" in error_text.lower():
            st.error(
                "Groq daily token limit reached. Please try again later, "
                "switch to a different model in config.py, or upgrade your "
                "Groq plan."
            )
            st.caption(error_text)
        elif "GROQ_API_KEY" in error_text or "401" in error_text:
            st.error(f"Analysis failed: {exc}")
            st.info(
                "Check that GROQ_API_KEY is configured in Streamlit Cloud "
                "Secrets and redeploy the app."
            )
        else:
            st.error(f"Analysis failed: {exc}")
        st.stop()

    progress.progress(100)
    status.success("Analysis completed.")

    st.divider()

    report = result["report"]
    scores = result["scores"]

    # Dashboard
    st.subheader("📊 Startup Validation Dashboard")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Validation Readiness", f'{scores["overall"]}/100')
    c2.metric("Evidence Strength", report["evidence_strength"])
    c3.metric("Biggest Risk", report["biggest_risk"])
    c4.metric("Biggest Unknown", report["biggest_unknown"])

    st.markdown("### Category Assessments")

    score_cols = st.columns(3)
    for index, (name, value) in enumerate(scores["categories"].items()):
        score_cols[index % 3].metric(name, f"{value}/100")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("💪 Biggest Strength")
        st.write(report["biggest_strength"])

        st.subheader("❓ Biggest Unknown")
        st.write(report["biggest_unknown"])

    with right:
        st.subheader("⚠️ Biggest Risk")
        st.write(report["biggest_risk"])

        st.subheader("➡️ Recommended Next Action")
        st.write(report["next_action"])

    st.divider()

    # Agent activity/results
    with st.expander("🤖 Agent Analysis", expanded=False):
        for item in result["agent_results"]:
            st.markdown(f"#### {item['agent']}")
            st.write(item["summary"])
            st.caption(
                f"Score: {item['score']}/100 | Confidence: {item['confidence']}"
            )

            if item.get("evidence"):
                st.markdown("**Evidence**")
                for evidence in item["evidence"]:
                    st.write(f"- {evidence}")

            if item.get("unknowns"):
                st.markdown("**Unknowns**")
                for unknown in item["unknowns"]:
                    st.write(f"- {unknown}")

    # Evidence
    st.subheader("🔎 Evidence & Sources")
    if result["research"]:
        st.markdown(result["research"])
    else:
        st.info("No external research was returned.")

    # Red team
    st.subheader("🔴 Red-Team Findings")
    for finding in result["red_team"]["challenges"]:
        st.write(f"- {finding}")

    st.markdown("**Critical assumptions challenged:**")
    for assumption in result["red_team"]["critical_assumptions"]:
        st.write(f"- {assumption}")

    # Validation plan
    st.subheader("🧪 Validation Plan")
    for item in result["validation"]["experiments"]:
        st.markdown(f"**{item['assumption']}**")
        st.write(f"- Experiment: {item['experiment']}")
        st.write(f"- Success criterion: {item['success_criterion']}")
        st.write(f"- Priority: {item['priority']}")

    st.subheader("📅 7-Day Validation Roadmap")
    for day in result["validation"]["seven_day_plan"]:
        st.write(f"**Day {day['day']}:** {day['action']}")

    # Final report
    st.subheader("📄 Final Report")

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
            st.write(content)

    st.success(
        f"Decision focus: {report['decision_focus']}"
    )
