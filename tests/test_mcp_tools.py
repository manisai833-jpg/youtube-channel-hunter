import unittest
from unittest.mock import Mock, patch

import httpx

from mcp.tools import search_youtube


class SearchYouTubeTests(unittest.TestCase):
    @patch("mcp.tools.httpx.get")
    def test_normalizes_query_before_request(self, mock_get):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {"channels": []}
        mock_get.return_value = response

        result = search_youtube("  test channel  ", limit=5)

        self.assertEqual(result, {"channels": []})
        self.assertEqual(
            mock_get.call_args.kwargs["params"],
            {"channel": "test channel", "limit": 5},
        )

    @patch("mcp.tools.httpx.get")
    def test_rejects_non_object_json_response(self, mock_get):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = ["unexpected"]
        mock_get.return_value = response

        result = search_youtube("test", limit=5)

        self.assertEqual(
            result,
            {
                "success": False,
                "error": "YouTube API returned an invalid response.",
            },
        )

    @patch("mcp.tools.httpx.get")
    def test_surfaces_api_error_message(self, mock_get):
        request = httpx.Request("GET", "https://example.test")
        mock_get.return_value = httpx.Response(
            429,
            request=request,
            json={"error": "YouTube API quota exceeded."},
        )

        result = search_youtube("test", limit=5)

        self.assertEqual(
            result,
            {
                "success": False,
                "error": "YouTube API quota exceeded.",
            },
        )


if __name__ == "__main__":
    unittest.main()
