"""Story 6.5c migration chain static checks."""
from pathlib import Path


VERSIONS = Path(__file__).resolve().parents[1] / "migrations" / "versions"


def test_story_6_5c_migration_chain():
    files = {
        "084_story_6_5c_ref_brand_posture.py": ('revision = "084"', 'down_revision = "083"'),
        "085_story_6_5c_company_brand_posture_fk.py": ('revision = "085"', 'down_revision = "084"'),
        "086_story_6_5c_block_f_component_capability.py": (
            'revision = "086"',
            'down_revision = "085"',
        ),
    }
    for name, markers in files.items():
        text = (VERSIONS / name).read_text(encoding="utf-8")
        for marker in markers:
            assert marker in text, f"{name} missing {marker}"


def test_story_6_5c_migrations_seed_brand_posture_and_block_f():
    combined = "\n".join(
        (VERSIONS / name).read_text(encoding="utf-8")
        for name in (
            "084_story_6_5c_ref_brand_posture.py",
            "085_story_6_5c_company_brand_posture_fk.py",
            "086_story_6_5c_block_f_component_capability.py",
        )
    )
    assert "ref.BrandPosture" in combined or "[ref].[BrandPosture]" in combined
    assert "BrandPostureID" in combined
    assert "COMPONENT_CAPABILITY" in combined
    assert "DynamicComponentCatalog" in combined
    assert "NVARCHAR(30)" in combined or "ALTER COLUMN [DataStructureType] NVARCHAR(30)" in combined
