import pytest
from unittest.mock import patch


class TestBuildSamplingHandler:
    @patch.dict("os.environ", {"ANTHROPIC_API_KEY": "", "ANTHROPIC_MODEL": ""}, clear=False)
    def test_returns_none_when_api_key_empty(self):
        import importlib
        import app.constants

        importlib.reload(app.constants)
        import lib.sampling

        importlib.reload(lib.sampling)

        from lib.sampling import build_sampling_handler

        result = build_sampling_handler()
        assert result is None

    @patch.dict("os.environ", {}, clear=False)
    def test_returns_none_when_api_key_missing(self):
        import os

        os.environ.pop("ANTHROPIC_API_KEY", None)

        import importlib
        import app.constants

        importlib.reload(app.constants)
        import lib.sampling

        importlib.reload(lib.sampling)

        from lib.sampling import build_sampling_handler

        result = build_sampling_handler()
        assert result is None

    @patch.dict("os.environ", {"ANTHROPIC_API_KEY": "sk-ant-test123"}, clear=False)
    def test_returns_none_when_anthropic_not_installed(self):
        import importlib
        import app.constants

        importlib.reload(app.constants)
        import lib.sampling

        importlib.reload(lib.sampling)

        from lib.sampling import build_sampling_handler

        with patch.dict("sys.modules", {"anthropic": None}):
            result = build_sampling_handler()

        assert result is None

    @patch.dict(
        "os.environ",
        {"ANTHROPIC_API_KEY": "sk-ant-test123", "ANTHROPIC_MODEL": "claude-haiku-4-5-20251001"},
        clear=False,
    )
    def test_returns_handler_when_configured(self):
        import importlib
        import app.constants

        importlib.reload(app.constants)
        import lib.sampling

        importlib.reload(lib.sampling)

        from lib.sampling import build_sampling_handler

        try:
            from fastmcp.client.sampling.handlers.anthropic import AnthropicSamplingHandler
        except ImportError:
            pytest.skip("anthropic package not installed")

        result = build_sampling_handler()
        assert isinstance(result, AnthropicSamplingHandler)
