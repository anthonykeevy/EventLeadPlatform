"""One-off UAT check for forms 504 (AU) vs 813 (UK event)."""
from sqlalchemy import create_engine, text
import os

url = os.getenv("DATABASE_URL") or (
    "mssql+pyodbc://localhost/EventLeadPlatform?"
    "driver=ODBC+Driver+18+for+SQL+Server&Trusted_Connection=Yes&TrustServerCertificate=yes"
)
engine = create_engine(url)

with engine.connect() as conn:
    print("=== Events 39 / 40 ===")
    for row in conn.execute(
        text(
            """
            SELECT e.EventID, e.Name, e.CountryID, c.CountryCode, c.CountryName
            FROM dbo.Event e
            LEFT JOIN ref.Country c ON c.CountryID = e.CountryID
            WHERE e.EventID IN (39, 40)
            """
        )
    ):
        print(dict(row._mapping))

    print("\n=== Forms 504 / 813 ===")
    for row in conn.execute(
        text(
            """
            SELECT f.FormID, e.EventID, e.Name AS EventName,
                   e.CountryID, c.CountryCode
            FROM dbo.Form f
            JOIN dbo.Event e ON e.EventID = f.EventID
            LEFT JOIN ref.Country c ON c.CountryID = e.CountryID
            WHERE f.FormID IN (504, 813)
            """
        )
    ):
        print(dict(row._mapping))

    print("\n=== Country-scoped FormBuilderComponent rows ===")
    rows = conn.execute(
        text(
            """
            SELECT fbc.ComponentCode, cs.ScopeCode, c.CountryCode
            FROM dbo.FormBuilderComponent fbc
            JOIN ref.ComponentScope cs ON fbc.ComponentScopeID = cs.ComponentScopeID
            LEFT JOIN ref.Country c ON c.CountryID = fbc.CountryID
            WHERE fbc.IsActive = 1 AND fbc.IsDeleted = 0
              AND cs.ScopeCode = 'Country'
            """
        )
    ).fetchall()
    print(f"Count: {len(rows)}")
    for r in rows:
        print(dict(r._mapping))

    print("\n=== Global catalog count ===")
    n = conn.execute(
        text(
            """
            SELECT COUNT(*)
            FROM dbo.FormBuilderComponent fbc
            JOIN ref.ComponentScope cs ON fbc.ComponentScopeID = cs.ComponentScopeID
            WHERE fbc.IsActive = 1 AND fbc.IsDeleted = 0 AND cs.ScopeCode = 'Global'
            """
        )
    ).scalar()
    print(n)

    import json

    print("\n=== Generation runs ===")
    for row in conn.execute(
        text(
            """
            SELECT GenerationRunID, FormID, TerminalReason, Status, CreatedDate
            FROM dbo.GenerationRun
            WHERE FormID IN (504, 813)
            ORDER BY GenerationRunID DESC
            """
        )
    ):
        print(dict(row._mapping))

    for gid, label in ((165, "504 AU"), (167, "813 GB after fix")):
        row = conn.execute(
            text(
                """
                SELECT ArtifactJson FROM dbo.GenerationArtifact
                WHERE GenerationRunID=:g AND ArtifactType='trace-metadata'
                """
            ),
            {"g": gid},
        ).fetchone()
        if not row:
            print(f"\nRun {gid}: no trace-metadata")
            continue
        s = row[0]
        print(f"\n=== Run {gid} ({label}) prompt/locale markers in trace ===")
        for needle in (
            "Audience locale UK",
            "Audience locale AU",
            "UK GDPR",
            "Privacy Act 1988",
            "British spelling",
            "Australian English",
            '"resolved":"UK"',
            '"resolved":"AU"',
            "Event.CountryID",
        ):
            print(f"  {needle}: {needle in s}")

