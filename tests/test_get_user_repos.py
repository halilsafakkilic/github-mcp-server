import pytest
from unittest.mock import patch

from app.services import get_user_repos


@pytest.mark.asyncio
class TestGetUserRepos:
    """Tests for the get_user_repos tool."""

    @patch("app.services.get_request")
    @patch("app.services.log_write_to_file")
    async def test_success_returns_repos(self, mock_log, mock_get, mock_ctx, mock_success_response, sample_repos):
        mock_get.return_value = mock_success_response

        result = await get_user_repos("testuser", mock_ctx)

        assert result["success"] is True
        assert result["data"]["username"] == "testuser"
        assert result["data"]["count"] == 2
        assert result["data"]["repositories"] == sample_repos

    @patch("app.services.get_request")
    @patch("app.services.log_write_to_file")
    async def test_success_context_info_called(self, mock_log, mock_get, mock_ctx, mock_success_response):
        mock_get.return_value = mock_success_response

        await get_user_repos("testuser", mock_ctx)

        mock_ctx.info.assert_any_call("Fetching repositories for user: testuser")
        mock_ctx.info.assert_any_call("Successfully fetched 2 repositories for user testuser")

    @patch("app.services.get_request")
    @patch("app.services.log_write_to_file")
    async def test_success_progress_reported(self, mock_log, mock_get, mock_ctx, mock_success_response):
        mock_get.return_value = mock_success_response

        await get_user_repos("testuser", mock_ctx)

        mock_ctx.report_progress.assert_any_call(0, 3, "Validating input")
        mock_ctx.report_progress.assert_any_call(1, 3, "Calling GitHub API")
        mock_ctx.report_progress.assert_any_call(2, 3, "Processing response")
        mock_ctx.report_progress.assert_any_call(3, 3, "Done")

    @patch("app.services.get_request")
    @patch("app.services.log_write_to_file")
    async def test_empty_repos(self, mock_log, mock_get, mock_ctx, mock_empty_repos_response):
        mock_get.return_value = mock_empty_repos_response

        result = await get_user_repos("emptyuser", mock_ctx)

        assert result["success"] is True
        assert result["data"]["repositories"] == []
        assert result["data"]["count"] == 0
        mock_ctx.info.assert_any_call("No repositories found for user: emptyuser")

    @patch("app.services.get_request")
    @patch("app.services.log_write_to_file")
    async def test_user_not_found_404(self, mock_log, mock_get, mock_ctx, mock_404_response):
        mock_get.return_value = mock_404_response

        result = await get_user_repos("ghost", mock_ctx)

        assert result["success"] is False
        assert result["error_code"] == "USER_NOT_FOUND"
        assert "ghost" in result["error"]
        mock_ctx.error.assert_any_call("User not found: ghost")

    @patch("app.services.get_request")
    @patch("app.services.log_write_to_file")
    async def test_api_error_500(self, mock_log, mock_get, mock_ctx, mock_500_response):
        mock_get.return_value = mock_500_response

        result = await get_user_repos("testuser", mock_ctx)

        assert result["success"] is False
        assert result["error_code"] == "API_ERROR"
        assert "500" in result["error"]
        mock_ctx.error.assert_any_call("GitHub API error for user testuser: 500")

    @patch("app.services.log_write_to_file")
    async def test_empty_username(self, mock_log, mock_ctx):
        result = await get_user_repos("", mock_ctx)

        assert result["success"] is False
        assert result["error_code"] == "INVALID_INPUT"
        mock_ctx.error.assert_called_once()

    @patch("app.services.log_write_to_file")
    async def test_whitespace_username(self, mock_log, mock_ctx):
        result = await get_user_repos("   ", mock_ctx)

        assert result["success"] is False
        assert result["error_code"] == "INVALID_INPUT"

    @patch("app.services.get_request")
    @patch("app.services.log_write_to_file")
    async def test_unexpected_exception(self, mock_log, mock_get, mock_ctx):
        mock_get.side_effect = ConnectionError("Network failure")

        result = await get_user_repos("testuser", mock_ctx)

        assert result["success"] is False
        assert result["error_code"] == "INTERNAL_ERROR"
        mock_ctx.error.assert_called_once()
        assert "Network failure" in str(mock_ctx.error.call_args)

    @patch("app.services.get_request")
    @patch("app.services.log_write_to_file")
    async def test_log_write_to_file_still_called(self, mock_log, mock_get, mock_ctx, mock_success_response):
        mock_get.return_value = mock_success_response

        await get_user_repos("testuser", mock_ctx)

        mock_log.assert_any_call("Fetching repositories for user: testuser")
        mock_log.assert_any_call("Successfully fetched 2 repositories for user testuser")
