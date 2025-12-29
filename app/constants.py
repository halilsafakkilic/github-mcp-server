import os
from dotenv import load_dotenv

load_dotenv()


def get_root_dir():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    return os.path.dirname(current_dir)


ROOT_DIR = get_root_dir()

SHTTP_PORT = int(os.getenv("SHTTP_PORT", 8080))
SSE_PORT = int(os.getenv("SSE_PORT", 8081))
GITHUB_API_TIMEOUT = int(os.getenv("GITHUB_API_TIMEOUT", 30))
