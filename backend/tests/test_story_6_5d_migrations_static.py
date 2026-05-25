"""Story 6.5d migration chain static checks."""
from pathlib import Path


VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"


def test_story_6_5d_migration_chain():
    files = {
        "087_story_6_5d_seed_global_catalog_backlog.py": ("087", "086"),
        "088_story_6_5d_edf_schema_and_au_components.py": ("088", "087"),
        "089_story_6_5d_ref_audience_locale.py": ("089", "088"),
        "090_story_6_5d_ref_form_purpose.py": ("090", "089"),
        "091_story_6_5d_ref_respondent_type.py": ("091", "090"),
        "092_story_6_5d_clarification_company_form_columns.py": ("092", "091"),
        "093_story_6_5d_generation_run_clarification_audit.py": ("093", "092"),
        "094_story_6_5d_block_e_clarification_registry.py": ("094", "093"),
        "095_story_6_5d_block_g_catalog_aligned_note.py": ("095", "094"),
    }
    for name, (rev, down) in files.items():
        text = (VERSIONS / name).read_text(encoding="utf-8")
        assert f'revision = "{rev}"' in text
        assert f'down_revision = "{down}"' in text


def test_story_6_5d_migrations_seed_edf_and_clarification():
    combined = "\n".join(
        (VERSIONS / name).read_text(encoding="utf-8")
        for name in (
            "087_story_6_5d_seed_global_catalog_backlog.py",
            "088_story_6_5d_edf_schema_and_au_components.py",
            "089_story_6_5d_ref_audience_locale.py",
            "090_story_6_5d_ref_form_purpose.py",
            "091_story_6_5d_ref_respondent_type.py",
            "094_story_6_5d_block_e_clarification_registry.py",
        )
    )
    assert "rating" in combined
    assert "address-lookup-au" in combined
    assert "company-lookup-abr" in combined
    assert "RequiresNetwork" in combined
    assert "ref.AudienceLocale" in combined or "[ref].[AudienceLocale]" in combined
    assert "CLARIFICATION_LOCALE" in combined or "E1" in combined
