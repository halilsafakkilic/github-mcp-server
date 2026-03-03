import json

import pytest
from unittest.mock import patch

from app.services import echo_resource, get_greeting, summarize_github_repos


@pytest.mark.asyncio
class TestEchoResource:
    @patch("app.services.log_write_to_file")
    async def test_returns_valid_json(self, mock_log):
        result = await echo_resource()
        data = json.loads(result)

        assert data["success"] is True
        assert data["data"]["message"] == "Echo!"

    @patch("app.services.log_write_to_file")
    async def test_logs_access(self, mock_log):
        await echo_resource()
        mock_log.assert_called_once_with("Echo resource accessed")


@pytest.mark.asyncio
class TestGetGreeting:
    @patch("app.services.log_write_to_file")
    async def test_returns_greeting_with_name(self, mock_log):
        result = await get_greeting("Alice")
        data = json.loads(result)

        assert data["success"] is True
        assert data["data"]["greeting"] == "Hello, Alice!"

    @patch("app.services.log_write_to_file")
    async def test_logs_name(self, mock_log):
        await get_greeting("Bob")
        mock_log.assert_called_once_with("Greeting requested for: Bob")


class TestSummarizeGithubReposPrompt:
    def test_returns_prompt_message(self):
        result = summarize_github_repos("some tool output")

        assert result.role == "user"
        assert result.content.type == "text"

    def test_includes_tool_output_in_text(self):
        result = summarize_github_repos('{"repos": []}')

        assert '{"repos": []}' in result.content.text

    def test_includes_rules(self):
        result = summarize_github_repos("data")

        assert "Sort by star count" in result.content.text
        assert "at most 5 repositories" in result.content.text
        assert "No public repositories found" in result.content.text
