"""
Tests for coerce_value() and merge_fields_with_stdin().
"""

import argparse
from unittest.mock import patch

import pytest
from pydantic import Field

from wekan.cli.handlers._helpers import (
    _resolve_field_info,
    coerce_value,
    merge_fields_with_stdin,
)
from wekan.client import WeKanModel

# ---------------------------------------------------------------------------
# Mock model with a variety of field types
# ---------------------------------------------------------------------------


class MockModel(WeKanModel):
    str_field: str = Field(default="", description="A string field")
    optional_str: str | None = Field(default=None, description="Optional string")
    int_field: int = Field(default=0, description="An integer field")
    optional_int: int | None = Field(default=None, description="Optional integer")
    float_field: float = Field(default=0.0, description="A float field")
    bool_field: bool = Field(default=False, description="A boolean field")
    str_list: list[str] = Field(default_factory=list, description="A list of strings")
    optional_str_list: list[str] | None = Field(
        default=None, description="Optional list"
    )
    edit_key_field: str | None = Field(
        default=None,
        description="Field with edit_key",
        json_schema_extra={"edit_key": "alias_name"},
    )


# ---------------------------------------------------------------------------
# _resolve_field_info
# ---------------------------------------------------------------------------


class TestResolveFieldInfo:
    def test_direct_lookup(self):
        fi = _resolve_field_info(MockModel, "str_field")
        assert fi is not None
        assert fi.description == "A string field"

    def test_edit_key_lookup(self):
        fi = _resolve_field_info(MockModel, "alias_name")
        assert fi is not None
        assert fi.description == "Field with edit_key"

    def test_unknown_field_returns_none(self):
        assert _resolve_field_info(MockModel, "nonexistent") is None


# ---------------------------------------------------------------------------
# coerce_value — schema-driven (with field_info)
# ---------------------------------------------------------------------------


class TestCoerceWithSchema:
    """Test coercion when field type info is available."""

    # -- str fields --

    @pytest.mark.parametrize(
        "value, expected",
        [
            ("hello", "hello"),
            ("123", "123"),
            ("true", "true"),
            ("null", "null"),
            ('"doublequoted"', "doublequoted"),
            ("'quoted'", "quoted"),
        ],
    )
    def test_str_field_passes_through(self, value, expected):
        fi = MockModel.model_fields["str_field"]
        assert coerce_value(value, fi) == expected

    # -- str | None fields --

    @pytest.mark.parametrize("value", ["", "null", "none", "None", "NULL"])
    def test_optional_str_null_variants(self, value):
        fi = MockModel.model_fields["optional_str"]
        assert coerce_value(value, fi) is None

    def test_optional_str_with_value(self):
        fi = MockModel.model_fields["optional_str"]
        assert coerce_value("hello", fi) == "hello"

    # -- bool fields --

    @pytest.mark.parametrize(
        "value, expected",
        [
            ("true", True),
            ("True", True),
            ("TRUE", True),
            ("false", False),
            ("False", False),
            ("FALSE", False),
            ("yes", True),
            ("no", False),
            ("Yes", True),
            ("No", False),
            ("YES", True),
            ("NO", False),
            ("other", False),
        ],
    )
    def test_bool_field(self, value, expected):
        fi = MockModel.model_fields["bool_field"]
        assert coerce_value(value, fi) is expected

    # -- int fields --

    @pytest.mark.parametrize(
        "value, expected",
        [
            ("0", 0),
            ("3", 3),
            ("-1", -1),
            ("999", 999),
        ],
    )
    def test_int_field(self, value, expected):
        fi = MockModel.model_fields["int_field"]
        assert coerce_value(value, fi) == expected

    def test_int_field_invalid_returns_string(self):
        fi = MockModel.model_fields["int_field"]
        assert coerce_value("abc", fi) == "abc"

    # -- int | None fields --

    def test_optional_int_null(self):
        fi = MockModel.model_fields["optional_int"]
        assert coerce_value("null", fi) is None

    def test_optional_int_with_value(self):
        fi = MockModel.model_fields["optional_int"]
        assert coerce_value("42", fi) == 42

    # -- float fields --

    @pytest.mark.parametrize(
        "value, expected",
        [
            ("1.5", 1.5),
            ("0.0", 0.0),
            ("-3.14", -3.14),
        ],
    )
    def test_float_field(self, value, expected):
        fi = MockModel.model_fields["float_field"]
        assert coerce_value(value, fi) == expected

    def test_float_field_int_string(self):
        fi = MockModel.model_fields["float_field"]
        assert coerce_value("3", fi) == 3.0

    def test_float_field_invalid_returns_string(self):
        fi = MockModel.model_fields["float_field"]
        assert coerce_value("abc", fi) == "abc"

    # -- list[str] fields --

    def test_list_single_value(self):
        fi = MockModel.model_fields["str_list"]
        assert coerce_value("one", fi) == ["one"]

    def test_list_comma_separated(self):
        fi = MockModel.model_fields["str_list"]
        assert coerce_value("a,b,c", fi) == ["a", "b", "c"]

    def test_list_comma_separated_with_spaces(self):
        fi = MockModel.model_fields["str_list"]
        assert coerce_value("a, b, c", fi) == ["a", "b", "c"]

    def test_list_json_array(self):
        fi = MockModel.model_fields["str_list"]
        assert coerce_value('["x","y"]', fi) == ["x", "y"]

    def test_list_invalid_json_falls_back_to_string(self):
        fi = MockModel.model_fields["str_list"]
        # Starts with [ but isn't valid JSON — treated as single-item list
        assert coerce_value("[broken", fi) == ["broken"]

    def test_list_quoted_csv(self):
        fi = MockModel.model_fields["str_list"]
        assert coerce_value('"key1","key2","key3"', fi) == ["key1", "key2", "key3"]

    def test_list_single_quoted_csv(self):
        fi = MockModel.model_fields["str_list"]
        assert coerce_value("'key1','key2','key3'", fi) == ["key1", "key2", "key3"]

    def test_list_bracketed_mixed_quotes(self):
        fi = MockModel.model_fields["str_list"]
        assert coerce_value("""["key1","key2",'key3',key4]""", fi) == [
            "key1", "key2", "key3", "key4",
        ]

    def test_list_single_quoted_value(self):
        fi = MockModel.model_fields["str_list"]
        assert coerce_value("'one'", fi) == ["one"]

    # -- list[str] | None fields --

    def test_optional_list_null(self):
        fi = MockModel.model_fields["optional_str_list"]
        assert coerce_value("null", fi) is None

    def test_optional_list_with_values(self):
        fi = MockModel.model_fields["optional_str_list"]
        assert coerce_value("a,b", fi) == ["a", "b"]


# ---------------------------------------------------------------------------
# coerce_value — heuristic fallback (no field_info)
# ---------------------------------------------------------------------------


class TestCoerceHeuristic:
    """Test coercion when no field type info is available."""

    @pytest.mark.parametrize("value", ["null", "none", "None", "NULL"])
    def test_null_keywords(self, value):
        assert coerce_value(value, None) is None

    def test_true(self):
        assert coerce_value("true", None) is True

    def test_false(self):
        assert coerce_value("false", None) is False

    def test_json_array(self):
        assert coerce_value('["a","b"]', None) == ["a", "b"]

    def test_json_object(self):
        assert coerce_value('{"k":"v"}', None) == {"k": "v"}

    def test_invalid_json_returns_string(self):
        assert coerce_value("[broken", None) == "[broken"

    def test_plain_string(self):
        assert coerce_value("hello world", None) == "hello world"

    def test_number_stays_string(self):
        # Without schema, numbers stay as strings to avoid ambiguity
        assert coerce_value("42", None) == "42"


# ---------------------------------------------------------------------------
# merge_fields_with_stdin
# ---------------------------------------------------------------------------


def _make_args(**kwargs) -> argparse.Namespace:
    """Build a Namespace with defaults for fields/use_json."""
    defaults = {"fields": None, "use_json": False}
    defaults.update(kwargs)
    return argparse.Namespace(**defaults)


class TestMergeFieldsWithStdin:
    def test_no_fields_no_json(self):
        args = _make_args()
        assert merge_fields_with_stdin(args) == {}

    def test_cli_fields_without_model(self):
        args = _make_args(fields={"str_field": "hello", "int_field": "3"})
        result = merge_fields_with_stdin(args)
        # Without model, values stay as strings (except heuristic matches)
        assert result == {"str_field": "hello", "int_field": "3"}

    def test_cli_fields_with_model(self):
        args = _make_args(
            fields={"str_field": "hello", "int_field": "3", "bool_field": "true"}
        )
        result = merge_fields_with_stdin(args, MockModel)
        assert result["str_field"] == "hello"
        assert result["int_field"] == 3
        assert result["bool_field"] is True

    def test_cli_list_field_with_model(self):
        args = _make_args(fields={"str_list": "a,b,c"})
        result = merge_fields_with_stdin(args, MockModel)
        assert result["str_list"] == ["a", "b", "c"]

    @patch("wekan.cli.handlers._helpers.read_json_stdin")
    def test_json_only(self, mock_stdin):
        mock_stdin.return_value = {"str_field": "from json", "int_field": 5}
        args = _make_args(use_json=True)
        result = merge_fields_with_stdin(args, MockModel)
        # JSON values are already typed, not coerced
        assert result == {"str_field": "from json", "int_field": 5}

    @patch("wekan.cli.handlers._helpers.read_json_stdin")
    def test_cli_overrides_json(self, mock_stdin):
        mock_stdin.return_value = {"str_field": "from json", "int_field": 10}
        args = _make_args(use_json=True, fields={"str_field": "from cli"})
        result = merge_fields_with_stdin(args, MockModel)
        assert result["str_field"] == "from cli"
        assert result["int_field"] == 10

    @patch("wekan.cli.handlers._helpers.read_json_stdin")
    def test_json_values_not_coerced(self, mock_stdin):
        """JSON values that are already typed should not be re-coerced."""
        mock_stdin.return_value = {
            "str_list": ["already", "a", "list"],
            "bool_field": True,
        }
        args = _make_args(use_json=True)
        result = merge_fields_with_stdin(args, MockModel)
        assert result["str_list"] == ["already", "a", "list"]
        assert result["bool_field"] is True

    def test_unknown_field_uses_heuristic(self):
        args = _make_args(fields={"unknown_field": "true"})
        result = merge_fields_with_stdin(args, MockModel)
        # Field not in model → heuristic fallback → "true" becomes True
        assert result["unknown_field"] is True

    def test_edit_key_resolution(self):
        args = _make_args(fields={"alias_name": "null"})
        result = merge_fields_with_stdin(args, MockModel)
        # alias_name resolves to the "edit_key_field" field (str | None) → None
        assert result["alias_name"] is None
