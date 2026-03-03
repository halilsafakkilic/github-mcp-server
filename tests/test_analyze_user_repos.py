import pytest
from unittest.mock import patch, MagicMock

from app.services import analyze_user_repos


@pytest.mark.asyncio
class TestAnalyzeUserRepos:
    """Tests for the analyze_user_repos tool (Sampling)."""

    @patch("app.services.get_request")
    async def test_success_returns_llm_text(self, mock_get, mock_ctx, mock_success_response):
        mock_get.return_value = mock_success_response
        mock_ctx.sample.return_value = MagicMock(text="User has 2 repos: repo-alpha (Python) and repo-beta (JS).")

        result = await analyze_user_repos("testuser", mock_ctx)

        assert "repo-alpha" in result or "2 repos" in result
        assert isinstance(result, str)

    @patch("app.services.get_request")
    async def test_sample_called_with_correct_params(self, mock_get, mock_ctx, mock_success_response):
        mock_get.return_value = mock_success_response
        mock_ctx.sample.return_value = MagicMock(text="Summary text")

        await analyze_user_repos("testuser", mock_ctx)

        mock_ctx.sample.assert_called_once()
        call_kwargs = mock_ctx.sample.call_args
        assert "Summarize these GitHub repositories" in call_kwargs.kwargs["messages"]
        assert call_kwargs.kwargs["system_prompt"] is not None
        assert call_kwargs.kwargs["max_tokens"] == 512

    @patch("app.services.get_request")
    async def test_repos_json_included_in_sample_messages(self, mock_get, mock_ctx, mock_success_response):
        mock_get.return_value = mock_success_response
        mock_ctx.sample.return_value = MagicMock(text="Summary")

        await analyze_user_repos("testuser", mock_ctx)

        messages = mock_ctx.sample.call_args.kwargs["messages"]
        assert "repo-alpha" in messages
        assert "repo-beta" in messages

    @patch("app.services.get_request")
    async def test_context_info_called_on_success(self, mock_get, mock_ctx, mock_success_response):
        mock_get.return_value = mock_success_response
        mock_ctx.sample.return_value = MagicMock(text="Summary")

        await analyze_user_repos("testuser", mock_ctx)

        mock_ctx.info.assert_any_call("Starting analysis for user: testuser")
        mock_ctx.info.assert_any_call("Fetched 2 repositories, sending to LLM for analysis")
        mock_ctx.info.assert_any_call("LLM analysis complete")

    @patch("app.services.get_request")
    async def test_api_error_returns_error_string(self, mock_get, mock_ctx, mock_500_response):
        mock_get.return_value = mock_500_response

        result = await analyze_user_repos("testuser", mock_ctx)

        assert "Error fetching repositories" in result
        assert "500" in result
        mock_ctx.error.assert_called_once()

    @patch("app.services.get_request")
    async def test_api_404_returns_error_string(self, mock_get, mock_ctx, mock_404_response):
        mock_get.return_value = mock_404_response

        result = await analyze_user_repos("ghost", mock_ctx)

        assert "Error fetching repositories" in result
        assert "404" in result

    @patch("app.services.get_request")
    async def test_unexpected_exception_returns_error_string(self, mock_get, mock_ctx):
        mock_get.side_effect = ConnectionError("DNS resolution failed")

        result = await analyze_user_repos("testuser", mock_ctx)

        assert "Error during analysis" in result
        assert "DNS resolution failed" in result
        mock_ctx.error.assert_called_once()

    @patch("app.services.get_request")
    async def test_sample_exception_caught(self, mock_get, mock_ctx, mock_success_response):
        mock_get.return_value = mock_success_response
        mock_ctx.sample.side_effect = RuntimeError("Sampling not supported by client")

        result = await analyze_user_repos("testuser", mock_ctx)

        assert "Error during analysis" in result
        assert "Sampling not supported" in result
