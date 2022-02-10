import pytest
from fb_group.utils import parse_args


class TestUtils:
    def test_parse_args(self):
        assert parse_args([]) == {}
        assert parse_args(["a=1"]) == {"a": "1"}
        assert parse_args(["a=1", "b=2"]) == {"a": "1", "b": "2"}
        assert parse_args(["a"]) == {}
        assert parse_args(["a", "b"]) == {}
        assert parse_args(["a="]) == {"a": ""}
        assert parse_args(["a=", "b="]) == {"a": "", "b": ""}
