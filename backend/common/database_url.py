"""
Resolve DATABASE_URL for SQLAlchemy from multiple input shapes used on Azure and locally.

Supports:
- Full SQLAlchemy URL: mssql+pyodbc://...
- ODBC connection strings (semicolon-separated, as often pasted from Azure Portal / ADO.NET docs)
- Discrete AZURE_SQL_* app settings (avoids URL-encoding passwords in a single DATABASE_URL)
"""
from __future__ import annotations

import os
import re
from urllib.parse import quote_plus

DEFAULT_LOCAL_SQL = (
    "mssql+pyodbc://localhost/EventLeadPlatform?"
    "driver=ODBC+Driver+18+for+SQL+Server&Trusted_Connection=Yes&TrustServerCertificate=yes"
)


def _parse_server(server: str) -> tuple[str, int]:
    s = server.strip()
    if s.lower().startswith("tcp:"):
        s = s[4:].strip()
    if "," in s:
        host, port_s = s.rsplit(",", 1)
        return host.strip(), int(port_s.strip())
    return s, 1433


def _parse_odbc_kv(odbc: str) -> dict[str, str]:
    """Parse semicolon-separated ODBC connection string into normalised keys."""
    out: dict[str, str] = {}
    if not odbc.strip():
        return out
    parts = re.split(r";(?![^{}]*\})", odbc)
    for part in parts:
        part = part.strip()
        if not part or "=" not in part:
            continue
        key, _, val = part.partition("=")
        key_norm = key.strip().lower().replace(" ", "")
        val_stripped = val.strip()
        if key_norm == "driver" and val_stripped.startswith("{") and val_stripped.endswith("}"):
            val_stripped = val_stripped[1:-1].strip()
        out[key_norm] = val_stripped
    return out


def odbc_connection_string_to_sqlalchemy(odbc: str) -> str:
    """
    Convert ODBC-style string to mssql+pyodbc URL for SQLAlchemy.

    Example input:
    Driver={ODBC Driver 18 for SQL Server};Server=tcp:host.database.windows.net,1433;...
    """
    kv = _parse_odbc_kv(odbc)
    if not kv:
        raise ValueError("Empty or unparseable ODBC connection string")

    driver_human = kv.get("driver", "ODBC Driver 18 for SQL Server")

    server = kv.get("server", "")
    if not server:
        raise ValueError("ODBC connection string missing Server=")

    database = kv.get("database", "")
    if not database:
        raise ValueError("ODBC connection string missing Database=")

    user = kv.get("uid") or kv.get("userid") or kv.get("user") or ""
    pwd = kv.get("pwd") or kv.get("password") or ""

    host, port = _parse_server(server)

    qparts = [
        f"driver={quote_plus(driver_human)}",
    ]
    if "encrypt" in kv:
        qparts.append(f"Encrypt={quote_plus(kv['encrypt'])}")
    if "trustservercertificate" in kv:
        qparts.append(f"TrustServerCertificate={quote_plus(kv['trustservercertificate'])}")
    if "connectiontimeout" in kv:
        qparts.append(f"Connection+Timeout={quote_plus(kv['connectiontimeout'])}")

    query = "&".join(qparts)
    return (
        f"mssql+pyodbc://{quote_plus(user)}:{quote_plus(pwd)}"
        f"@{host}:{port}/{database}?{query}"
    )


def _build_from_azure_sql_env() -> str | None:
    server = (os.getenv("AZURE_SQL_SERVER") or "").strip()
    database = (os.getenv("AZURE_SQL_DATABASE") or "").strip()
    user = (os.getenv("AZURE_SQL_USER") or os.getenv("AZURE_SQL_USERNAME") or "").strip()
    password = (os.getenv("AZURE_SQL_PASSWORD") or "").strip()
    if not (server and database and user and password):
        return None

    host, port = _parse_server(server)
    driver_human = (os.getenv("AZURE_SQL_ODBC_DRIVER") or "ODBC Driver 18 for SQL Server").strip()
    encrypt = (os.getenv("AZURE_SQL_ENCRYPT") or "yes").strip()
    trust = (os.getenv("AZURE_SQL_TRUST_SERVER_CERTIFICATE") or "no").strip()

    qparts = [
        f"driver={quote_plus(driver_human)}",
        f"Encrypt={quote_plus(encrypt)}",
        f"TrustServerCertificate={quote_plus(trust)}",
    ]
    timeout = (os.getenv("AZURE_SQL_CONNECTION_TIMEOUT") or "").strip()
    if timeout:
        qparts.append(f"Connection+Timeout={quote_plus(timeout)}")

    query = "&".join(qparts)
    return (
        f"mssql+pyodbc://{quote_plus(user)}:{quote_plus(password)}"
        f"@{host}:{port}/{database}?{query}"
    )


def _looks_like_odbc_connection_string(s: str) -> bool:
    t = s.strip()
    if not t:
        return False
    tl = t.lower()
    return "driver=" in tl and "server=" in tl


def resolve_database_url() -> str:
    """
    Return SQLAlchemy database URL. Also understands ODBC ADO-style DATABASE_URL values.
    """
    # Discrete Azure vars take precedence (clear split settings in Portal)
    built = _build_from_azure_sql_env()
    if built is not None:
        return built

    raw = (os.getenv("DATABASE_URL") or "").strip()

    if raw.startswith("mssql+pyodbc://") or raw.startswith("sqlite"):
        return raw

    if raw and _looks_like_odbc_connection_string(raw):
        try:
            return odbc_connection_string_to_sqlalchemy(raw)
        except Exception:
            pass

    if raw:
        if "Driver" in raw or "SERVER=" in raw.upper():
            try:
                return odbc_connection_string_to_sqlalchemy(raw)
            except Exception:
                pass
        return raw

    return DEFAULT_LOCAL_SQL


def sync_database_url_env() -> str:
    """
    Resolve URL and set os.environ['DATABASE_URL'] so Alembic and other tools see one value.
    """
    url = resolve_database_url()
    os.environ["DATABASE_URL"] = url
    return url
