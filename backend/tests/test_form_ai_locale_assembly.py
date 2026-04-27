from modules.form_ai import service


class _FakeResult:
    def __init__(self, *, row=None, first=None, all_rows=None):
        self._row = row
        self._first = first
        self._all_rows = all_rows if all_rows is not None else []

    def fetchone(self):
        return self._row

    def scalar_one_or_none(self):
        return self._row[0] if self._row else None

    def mappings(self):
        return self

    def first(self):
        return self._first

    def all(self):
        return self._all_rows


class _LocaleSession:
    def __init__(self, *, blocks=None, fallback_blocks=None):
        self.blocks = blocks if blocks is not None else {
            "format": "AU format block",
            "policy": "AU policy block",
            "tone": "AU tone block",
        }
        self.fallback_blocks = fallback_blocks if fallback_blocks is not None else {
            "format": "NEUTRAL format block",
            "policy": "NEUTRAL policy block",
            "tone": "NEUTRAL tone block",
        }
        self.block_query_count = 0
        self.logged_fallback = False

    def execute(self, statement, params=None):
        sql = " ".join(str(statement).split())
        params = params or {}
        if "FROM [ref].[Country]" in sql and "[CountryCode] = :country_code" in sql:
            return _FakeResult(row=(1 if params.get("country_code") == "AU" else None,))
        if "FROM [config].[PromptTemplateVersion]" in sql:
            return _FakeResult(
                first={
                    "PromptTemplateID": 10,
                    "PromptTemplateVersionID": 20,
                }
            )
        if "FROM [config].[PromptTemplateLocaleBlock]" in sql:
            self.block_query_count += 1
            source = self.fallback_blocks if params.get("country_id") is None else self.blocks
            return _FakeResult(
                all_rows=[
                    {"BlockType": block_type, "BlockBody": body}
                    for block_type, body in source.items()
                ]
            )
        if "INSERT INTO [log].[ApplicationError]" in sql:
            self.logged_fallback = True
            return _FakeResult()
        raise AssertionError(f"Unexpected SQL: {sql}")


def test_assemble_locale_block_registry_hit_and_cache():
    service._invalidate_locale_block_cache()
    session = _LocaleSession()

    first = service._assemble_locale_block("AU", "local", session)
    second = service._assemble_locale_block("AU", "local", session)

    assert first == "AU format block\nAU policy block\nAU tone block"
    assert second == first
    assert session.block_query_count == 1


def test_assemble_locale_block_intl_online_uses_neutral_rows():
    service._invalidate_locale_block_cache()
    session = _LocaleSession()

    block = service._assemble_locale_block("INTL_ONLINE", "neutral", session)

    assert block == "NEUTRAL format block\nNEUTRAL policy block\nNEUTRAL tone block"


def test_assemble_locale_block_missing_country_rows_falls_back_and_logs():
    service._invalidate_locale_block_cache()
    session = _LocaleSession(blocks={"format": "AU format only"})

    block = service._assemble_locale_block("AU", "local", session)

    assert block == "NEUTRAL format block\nNEUTRAL policy block\nNEUTRAL tone block"
    assert session.logged_fallback is True
