"""Output exporters: Markdown, CSV, and Excel generation for results."""

from __future__ import annotations

import io
import csv as csv_module

import pandas as pd


def to_csv_bytes(rows: list[dict[str, str]]) -> bytes:
    """Serialize a list of row dicts to CSV bytes (UTF-8)."""
    if not rows:
        return b""
    buffer = io.StringIO()
    writer = csv_module.DictWriter(buffer, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def to_xlsx_bytes(rows: list[dict[str, str]]) -> bytes:
    """Serialize a list of row dicts to Excel bytes (xlsx)."""
    if not rows:
        return b""
    df = pd.DataFrame(rows)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Test Cases")
    return buffer.getvalue()


def render_download_buttons(markdown_text: str, rows: list[dict[str, str]], key_prefix: str) -> None:
    """Render st.download_button widgets for Markdown/CSV/Excel (imports streamlit lazily)."""
    import streamlit as st

    if rows:
        csv_bytes = to_csv_bytes(rows)
        xlsx_bytes = to_xlsx_bytes(rows)
        st.download_button(
            "Download CSV",
            data=csv_bytes,
            file_name="test_cases.csv",
            mime="text/csv",
            key=f"{key_prefix}_csv",
        )
        st.download_button(
            "Download Excel",
            data=xlsx_bytes,
            file_name="test_cases.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"{key_prefix}_xlsx",
        )
    st.download_button(
        "Download Markdown",
        data=markdown_text.encode("utf-8"),
        file_name="test_cases.md",
        mime="text/markdown",
        key=f"{key_prefix}_md",
    )
