import pytest
from unittest.mock import AsyncMock


class MockContext:
    """Mock for fastmcp.Context that records all calls."""

    def __init__(self):
        self.info = AsyncMock()
        self.error = AsyncMock()
        self.debug = AsyncMock()
        self.warning = AsyncMock()
        self.report_progress = AsyncMock()
        self.sample = AsyncMock()


class MockResponse:
    """Mock for requests.Response."""

    def __init__(self, status_code: int, json_data=None, text: str = ""):
        self.status_code = status_code
        self._json_data = json_data
        self.text = text

    def json(self):
        return self._json_data


SAMPLE_REPOS = [
    {
        "name": "repo-alpha",
        "full_name": "testuser/repo-alpha",
        "description": "A test repository",
        "language": "Python",
        "stargazers_count": 42,
        "html_url": "https://github.com/testuser/repo-alpha",
    },
    {
        "name": "repo-beta",
        "full_name": "testuser/repo-beta",
        "description": "Another test repository",
        "language": "JavaScript",
        "stargazers_count": 10,
        "html_url": "https://github.com/testuser/repo-beta",
    },
]


@pytest.fixture
def mock_ctx():
    return MockContext()


@pytest.fixture
def sample_repos():
    return SAMPLE_REPOS


@pytest.fixture
def mock_success_response(sample_repos):
    return MockResponse(status_code=200, json_data=sample_repos)


@pytest.fixture
def mock_404_response():
    return MockResponse(status_code=404, text="Not Found")


@pytest.fixture
def mock_500_response():
    return MockResponse(status_code=500, text="Internal Server Error")


@pytest.fixture
def mock_empty_repos_response():
    return MockResponse(status_code=200, json_data=[])
