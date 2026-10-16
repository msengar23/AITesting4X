"""Tests for output exporters."""

from output_exporter import to_csv_bytes, to_xlsx_bytes

ROWS = [
    {"TC ID": "TC-001", "Scenario": "Login works", "Priority": "High"},
    {"TC ID": "TC-002", "Scenario": "Login fails", "Priority": "Medium"},
]


def test_to_csv_bytes_has_header_and_rows():
    data = to_csv_bytes(ROWS).decode("utf-8")
    assert "TC ID" in data
    assert "TC-001" in data
    assert "Login fails" in data


def test_to_xlsx_bytes_is_valid_xlsx():
    data = to_xlsx_bytes(ROWS)
    assert data[:2] == b"PK"  # xlsx is a zip
    assert len(data) > 100


def test_empty_rows_return_empty():
    assert to_csv_bytes([]) == b""
    assert to_xlsx_bytes([]) == b""
