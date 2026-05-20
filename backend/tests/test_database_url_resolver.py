"""Tests for ODBC / Azure DATABASE_URL resolution."""
import os

import pytest

from common.database_url import (
    odbc_connection_string_to_sqlalchemy,
    resolve_database_url,
)


def test_odbc_to_sqlalchemy_sample():
    odbc = (
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=tcp:signalplatforms-test-sql.database.windows.net,1433;"
        "Database=EventLeadPlatformTest;"
        "Uid=signaladmin;"
        "Pwd=MyP@ss#X;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    url = odbc_connection_string_to_sqlalchemy(odbc)
    assert url.startswith("mssql+pyodbc://")
    assert "signalplatforms-test-sql.database.windows.net" in url
    assert "EventLeadPlatformTest" in url
    assert "signaladmin" in url
    assert "MyP%40ss%23X" in url or "MyP%40ss" in url


def test_resolve_prefers_full_sqlalchemy():
    prev = dict(os.environ)
    try:
        os.environ.clear()
        os.environ.update(prev)
        os.environ["DATABASE_URL"] = (
            "mssql+pyodbc://u:p@host:1433/db?"
            "driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes"
        )
        assert resolve_database_url() == os.environ["DATABASE_URL"]
    finally:
        os.environ.clear()
        os.environ.update(prev)


def test_resolve_odbc_env(monkeypatch):
    monkeypatch.delenv("AZURE_SQL_SERVER", raising=False)
    monkeypatch.delenv("AZURE_SQL_DATABASE", raising=False)
    monkeypatch.setenv(
        "DATABASE_URL",
        "Driver={ODBC Driver 18 for SQL Server};Server=tcp:h.db.windows.net,1433;"
        "Database=DB;Uid=u;Pwd=p;",
    )
    url = resolve_database_url()
    assert url.startswith("mssql+pyodbc://")
    assert "h.db.windows.net" in url
