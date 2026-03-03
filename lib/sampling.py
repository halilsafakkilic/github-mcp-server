from app.constants import ANTHROPIC_API_KEY, ANTHROPIC_MODEL


def build_sampling_handler():
    """Return an AnthropicSamplingHandler if ANTHROPIC_API_KEY is configured, else None.

    Requirements:
        - ANTHROPIC_API_KEY must be set in .env
        - anthropic package must be installed: uv add anthropic  (or uv sync --extra sampling)
    """
    if not ANTHROPIC_API_KEY:
        return None

    try:
        from anthropic import AsyncAnthropic
        from fastmcp.client.sampling.handlers.anthropic import AnthropicSamplingHandler
    except ImportError:
        print(
            "Warning: sampling is disabled — 'anthropic' package not installed.\n"
            "Run: uv add anthropic  (or uv sync --extra sampling)"
        )
        return None

    return AnthropicSamplingHandler(
        default_model=ANTHROPIC_MODEL,
        client=AsyncAnthropic(api_key=ANTHROPIC_API_KEY),
    )
