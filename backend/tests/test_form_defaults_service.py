"""
Unit tests for Form Defaults service (Story 5.2 T02)
"""
import pytest
import json
from unittest.mock import MagicMock

from modules.form_defaults.service import deep_merge


class TestDeepMerge:
    """Test deep merge logic."""

    def test_merge_flat_keys(self):
        base = {"a": 1, "b": 2}
        override = {"b": 20, "c": 3}
        result = deep_merge(base, override)
        assert result == {"a": 1, "b": 20, "c": 3}

    def test_merge_nested_dict(self):
        base = {"theme": {"primaryColor": "#0055FF", "fontFamily": "Inter"}}
        override = {"theme": {"primaryColor": "#FF0000"}}
        result = deep_merge(base, override)
        assert result["theme"]["primaryColor"] == "#FF0000"
        assert result["theme"]["fontFamily"] == "Inter"

    def test_merge_default_grid_layouts(self):
        base = {"globalStyles": {"defaultGridLayoutsByComponent": {"text": {"vertical": {"rows": 3}}}}}
        override = {"globalStyles": {"defaultGridLayoutsByComponent": {"text": {"vertical": {"rows": 5}}}}}
        result = deep_merge(base, override)
        assert result["globalStyles"]["defaultGridLayoutsByComponent"]["text"]["vertical"]["rows"] == 5
