"""MCP tools for the YouTube Channel Hunter server."""

import httpx


def search_youtube(channel: str, limit: int = 5) -> dict:
    """Call the deployed YouTube search API and return its JSON response."""
    try:
        response = httpx.get(
            "https://youtube-channel-hunter.onrender.com/search",
            params={"channel": channel, "limit": limit},
            timeout=15.0,
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as exc:
        return {
            "success": False,
            "error": str(exc),
        }
    except httpx.RequestError as exc:
        return {
            "success": False,
            "error": str(exc),
        }
