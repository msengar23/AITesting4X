"""Streamlit entry point: two-page Jira AI Test Case Generator.

Run with: streamlit run app.py
"""

from __future__ import annotations

import logging
from pathlib import Path

import streamlit as st

from config_manager import ConfigManager
from errors import AppError
from jira_client import JiraClient
from llm_client import LLMClient
from output_exporter import render_download_buttons
from test_case_generator import generate
from utils import mask_secret, setup_logging

st.set_page_config(page_title="Jira AI Test Case Generator", page_icon="🐞", layout="wide")

logger = setup_logging(env_path=Path(__file__).resolve().parent / ".env")
config = ConfigManager()


def render_config_page() -> None:
    st.title("Jira & AI Configuration")
    st.caption("Credentials are stored in the local .env file (gitignored). Never commit them.")

    all_config = config.get_all()
    provider = config.provider()

    with st.form("config_form"):
        st.subheader("Jira")
        jira_url = st.text_input("Jira Base URL", value=all_config.get("JIRA_BASE_URL", ""))
        jira_email = st.text_input("Jira Email", value=all_config.get("JIRA_EMAIL", ""))
        jira_token = st.text_input(
            "Jira API Token",
            value=all_config.get("JIRA_API_TOKEN", ""),
            type="password",
            help="Masked in the UI. Stored in .env.",
        )

        st.subheader("LLM Provider")
        provider_choice = st.selectbox(
            "Provider",
            options=["ollama", "groq"],
            index=0 if provider == "ollama" else 1,
        )

        st.subheader("Ollama")
        ollama_url = st.text_input(
            "Ollama Base URL",
            value=all_config.get("OLLAMA_BASE_URL", ""),
        )
        ollama_model = st.text_input(
            "Ollama Model",
            value=all_config.get("OLLAMA_MODEL", ""),
        )

        st.subheader("Groq (fallback)")
        groq_key = st.text_input(
            "Groq API Key",
            value=all_config.get("GROQ_API_KEY", ""),
            type="password",
            help="Masked in the UI. Stored in .env.",
        )
        groq_model = st.text_input(
            "Groq Model",
            value=all_config.get("GROQ_MODEL", ""),
        )

        save = st.form_submit_button("Save Settings")
        validate = st.form_submit_button("Validate Connection")

    if save:
        updates = {
            "JIRA_BASE_URL": jira_url.strip(),
            "JIRA_EMAIL": jira_email.strip(),
            "JIRA_API_TOKEN": jira_token.strip(),
            "LLM_PROVIDER": provider_choice,
            "OLLAMA_BASE_URL": ollama_url.strip(),
            "OLLAMA_MODEL": ollama_model.strip(),
            "GROQ_API_KEY": groq_key.strip(),
            "GROQ_MODEL": groq_model.strip(),
        }
        try:
            config.save(updates)
            config.reload()
            st.success("Settings saved to .env.")
        except Exception as exc:  # noqa: BLE001
            st.error(f"Could not save settings: {exc}")

    if validate:
        try:
            config.validate()
            all_cfg = config.get_all()
            jira = JiraClient(all_cfg["JIRA_BASE_URL"], all_cfg["JIRA_EMAIL"], all_cfg["JIRA_API_TOKEN"])
            with st.spinner("Validating Jira connection..."):
                jira.verify_connection()
            llm = LLMClient(provider=config.provider(), config=all_cfg)
            with st.spinner(f"Validating {config.provider()} availability..."):
                llm.verify_available()
            st.success(f"Jira connection OK. {config.provider()} availability OK (model: {llm.model}).")
        except AppError as exc:
            st.error(exc.message)

    st.divider()
    st.subheader("Current configuration")
    safe = {
        "Jira Base URL": all_config.get("JIRA_BASE_URL") or "—",
        "Jira Email": all_config.get("JIRA_EMAIL") or "—",
        "Jira API Token": mask_secret(all_config.get("JIRA_API_TOKEN")) or "—",
        "Provider": provider,
        "Ollama URL": all_config.get("OLLAMA_BASE_URL") or "—",
        "Ollama Model": all_config.get("OLLAMA_MODEL") or "—",
        "Groq API Key": mask_secret(all_config.get("GROQ_API_KEY")) or "—",
        "Groq Model": all_config.get("GROQ_MODEL") or "—",
    }
    st.json(safe)


def render_chat_page() -> None:
    st.title("AI Test Case Generator")
    st.caption(
        "ChatGPT-like interface. Ask for test cases or a test plan for a Jira issue "
        "using its key, e.g. **PROJ-123**. The app fetches the issue from Jira and "
        "grounds the LLM output strictly in the retrieved content."
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        st.subheader("Active provider")
        provider = config.provider()
        if provider == "groq":
            model = config.get("GROQ_MODEL")
        else:
            model = config.get("OLLAMA_MODEL")
        st.info(f"**{provider.capitalize()}** / {model or 'not set'}")
        if st.button("Clear chat"):
            st.session_state.messages = []
            st.rerun()

    # Example prompts to get the user started.
    with st.expander("Example requests", expanded=False):
        examples = [
            "Create positive and negative test cases for PROJ-123",
            "Create a complete test plan for PROJ-123",
            "Create boundary value analysis and equivalence partitioning test cases for PROJ-123",
            "Create security test cases including SQL injection for PROJ-123",
        ]
        for ex in examples:
            if st.button(ex, key=ex):
                st.session_state.messages.append({"role": "user", "content": ex})
                st.rerun()

    # Render chat history.
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("provider"):
                st.caption(f"Generated by {msg['provider']} / {msg['model']}")
                if msg.get("markdown") and msg.get("rows"):
                    render_download_buttons(msg["markdown"], msg["rows"], key_prefix=f"hist_{len(st.session_state.messages)}")

    prompt = st.chat_input("e.g. Create test cases for VWO-49")
    if prompt and prompt.strip():
        st.session_state.messages.append({"role": "user", "content": prompt.strip()})
        with st.chat_message("user"):
            st.markdown(prompt.strip())

        with st.chat_message("assistant"):
            try:
                with st.spinner("Fetching Jira issue and generating..."):
                    output = generate(prompt.strip(), config)
                st.markdown(output.raw_markdown)
                st.caption(f"Generated by {output.result.provider} / {output.result.model}")
                render_download_buttons(output.raw_markdown, output.table_rows, key_prefix=f"gen_{len(st.session_state.messages)}")
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": output.raw_markdown,
                        "provider": output.result.provider,
                        "model": output.result.model,
                        "markdown": output.raw_markdown,
                        "rows": output.table_rows,
                    }
                )
            except AppError as exc:
                st.error(exc.message)
                st.session_state.messages.append({"role": "assistant", "content": f"⚠️ {exc.message}"})


def main() -> None:
    page = st.sidebar.radio("Navigation", ["AI Test Case Generator", "Jira & AI Configuration"])
    if page == "AI Test Case Generator":
        render_chat_page()
    else:
        render_config_page()


if __name__ == "__main__":
    main()
