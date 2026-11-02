"""MCP tools for the YouTube Channel Hunter server."""

import httpx


def search_youtube(channel: str, limit: int = 5) -> dict:
    """Call the deployed YouTube search API and return its JSON response."""
    channel = channel.strip()
    if not channel:
        return {
            "success": False,
            "error": "Channel query cannot be blank.",
        }

    if len(channel) > 100:
        return {
            "success": False,
            "error": "Channel query must be 100 characters or fewer.",
        }

    if not 1 <= limit <= 50:
        return {
            "success": False,
            "error": "Limit must be between 1 and 50.",
        }

    try:
        response = httpx.get(
            "https://youtube-channel-hunter.onrender.com/search",
            params={"channel": channel, "limit": limit},
            timeout=15.0,
        )
        response.raise_for_status()
        response_data = response.json()
        if not isinstance(response_data, dict):
            return {
                "success": False,
                "error": "YouTube API returned an invalid response.",
            }
        return response_data
    except httpx.HTTPStatusError as exc:
        try:
            error_data = exc.response.json()
        except ValueError:
            error_data = {}
        error = None
        if isinstance(error_data, dict):
            error = error_data.get("detail") or error_data.get("error")
        return {
            "success": False,
            "error": error or str(exc),
        }
    except httpx.TimeoutException:
        return {
            "success": False,
            "error": "YouTube API request timed out. Please try again.",
        }
    except httpx.RequestError as exc:
        return {
            "success": False,
            "error": str(exc),
        }
    except ValueError:
        return {
            "success": False,
            "error": "YouTube API returned an invalid response.",
        }
