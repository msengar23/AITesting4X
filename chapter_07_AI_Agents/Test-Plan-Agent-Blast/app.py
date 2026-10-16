"""Streamlit UI for the Test Plan Agent.

A thin presentation shell over tools/pipeline.py (invariant I9: no pipeline
logic lives here). Run with:

    py -m streamlit run app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.config import Config, load_config  # noqa: E402
from tools.errors import AppError  # noqa: E402
from tools.pipeline import generate_test_plan  # noqa: E402
from tools.render_markdown import coverage_summary  # noqa: E402

st.set_page_config(page_title="Test Plan Agent", page_icon="🧪", layout="wide")

st.title("🧪 Test Plan Agent")
st.caption("Generate a Markdown test plan from a Jira issue ID.")

with st.sidebar:
    st.header("Configuration")
    try:
        config: Config | None = load_config()
    except AppError as exc:
        config = None
        st.error(exc.message)

    if config is not None:
        st.success("Configuration loaded")
        for key, value in config.masked().items():
            st.text(f"{key}: {value}")

    st.divider()
    st.caption(
        "Output is written to the project's `outputs/` folder. "
        "Plans are AI-generated drafts and require human review."
    )

with st.form("plan_form"):
    jira_key = st.text_input("Jira issue ID", placeholder="e.g. SAM1-1")
    instructions = st.text_area(
        "Additional instructions (optional)",
        placeholder="e.g. Focus on boundary values and negative cases",
        height=90,
    )
    submitted = st.form_submit_button("Generate test plan", type="primary")

if submitted:
    if config is None:
        st.stop()

    if not jira_key.strip():
        st.warning("Enter a Jira issue ID first.")
        st.stop()

    status = st.status("Starting…", expanded=True)
    try:
        with status:
            st.write("Loading configuration…")
            st.write(f"Fetching Jira issue {jira_key.strip().upper()}…")
            result = generate_test_plan(
                jira_key.strip(),
                instructions=instructions,
                config=config,
                on_stage=st.write,
            )
        status.update(label="Test plan generated", state="complete", expanded=False)
    except AppError as exc:
        status.update(label="Generation failed", state="error", expanded=False)
        st.error(exc.message)
        st.stop()
    except Exception as exc:  # noqa: BLE001 - never leak a traceback to the UI
        status.update(label="Generation failed", state="error", expanded=False)
        st.error("Something went wrong while generating the plan. Please try again.")
        st.caption(f"Internal detail: {type(exc).__name__}")
        st.stop()

    plan = result.plan
    cases = plan.get("test_cases", [])

    left, middle, right = st.columns(3)
    left.metric("Test cases", len(cases))
    middle.metric("Model", result.model.split("/")[-1])
    right.metric("Priority", result.issue.get("priority", "Unknown"))

    st.subheader(f"{result.issue.get('key')} — {result.issue.get('summary', '')}")
    st.info(
        "⚠️ AI-generated draft — requires human review. "
        "Open every case and add any missing domain scenarios."
    )
    action_left, action_right = st.columns([1, 1])
    with action_left:
        st.download_button(
            "Download Markdown",
            data=result.markdown.encode("utf-8"),
            file_name=result.output_path.name,
            mime="text/markdown",
            use_container_width=True,
        )
    with action_right:
        st.caption(f"Saved to `{result.output_path}`")

    preview_tab, summary_tab = st.tabs(["Full plan", "Coverage & risks"])
    with preview_tab:
        st.markdown(result.markdown)
    with summary_tab:
        st.markdown("**Coverage summary** (computed by code)")
        summary = coverage_summary(cases)
        st.write(f"Total cases: **{summary['total']}**")
        st.write("By priority: " + ", ".join(f"{k}: {v}" for k, v in summary["by_priority"].items()))
        st.write("By type: " + ", ".join(f"{k}: {v}" for k, v in summary["by_type"].items()))
        st.write(
            "By technique: "
            + ", ".join(f"{k}: {v}" for k, v in summary["by_technique"].items())
        )
        st.markdown("**Risks**")
        for risk in plan.get("risks", []):
            st.markdown(f"- {risk}")
        st.markdown("**Out of scope**")
        for item in plan.get("out_of_scope", []):
            st.markdown(f"- {item}")
