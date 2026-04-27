from pathlib import Path


MIGRATIONS_DIR = Path(__file__).resolve().parents[1] / "migrations" / "versions"


def test_story_6441_migration_chain_and_key_artifacts_present():
    expected = {
        "063_story_6441_prompt_template_locale_block.py": ('revision = "063"', 'down_revision = "062"'),
        "064_story_6441_country_cultural_dimensions.py": ('revision = "064"', 'down_revision = "063"'),
        "065_story_6441_seed_locale_blocks_au.py": ('revision = "065"', 'down_revision = "064"'),
        "066_story_6441_seed_locale_blocks_nz_uk_us_ca_ie.py": ('revision = "066"', 'down_revision = "065"'),
        "067_story_6441_seed_locale_blocks_intl_online.py": ('revision = "067"', 'down_revision = "066"'),
        "068_story_6441_seed_country_cultural_dimensions.py": ('revision = "068"', 'down_revision = "067"'),
        "069_story_6441_generation_run_brand_posture.py": ('revision = "069"', 'down_revision = "068"'),
        "070_story_6441_company_brand_posture.py": ('revision = "070"', 'down_revision = "069"'),
        "071_story_6441_app_settings_locale_defaults.py": ('revision = "071"', 'down_revision = "070"'),
    }

    for filename, required_snippets in expected.items():
        text = (MIGRATIONS_DIR / filename).read_text(encoding="utf-8")
        for snippet in required_snippets:
            assert snippet in text


def test_story_6441_migrations_cover_registry_resolution_contract():
    combined = "\n".join(
        (MIGRATIONS_DIR / filename).read_text(encoding="utf-8")
        for filename in (
            "063_story_6441_prompt_template_locale_block.py",
            "064_story_6441_country_cultural_dimensions.py",
            "069_story_6441_generation_run_brand_posture.py",
            "070_story_6441_company_brand_posture.py",
            "071_story_6441_app_settings_locale_defaults.py",
        )
    )

    assert "PromptTemplateLocaleBlock" in combined
    assert "CountryCulturalDimensions" in combined
    assert "BrandPosture" in combined
    assert "BrandHeritageOrigin" in combined
    assert "form_ai.default_audience_locale" in combined
    assert "form_ai.default_brand_posture" in combined
    assert "form_ai.locale_block_render_strategy" in combined
