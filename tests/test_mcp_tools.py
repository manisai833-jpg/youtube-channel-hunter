import unittest
from unittest.mock import Mock, patch

import httpx

from mcp.tools import search_youtube


class SearchYouTubeTests(unittest.TestCase):
    @patch("mcp.tools.httpx.get")
    def test_rejects_blank_query_before_request(self, mock_get):
        result = search_youtube("   ", limit=5)

        self.assertEqual(
            result,
            {
                "success": False,
                "error": "Channel query cannot be blank.",
            },
        )
        mock_get.assert_not_called()

    @patch("mcp.tools.httpx.get")
    def test_rejects_oversized_query_before_request(self, mock_get):
        result = search_youtube("x" * 101, limit=5)

        self.assertEqual(
            result,
            {
                "success": False,
                "error": "Channel query must be 100 characters or fewer.",
            },
        )
        mock_get.assert_not_called()

    @patch("mcp.tools.httpx.get")
    def test_rejects_out_of_range_limit_before_request(self, mock_get):
        for limit in (0, 51):
            with self.subTest(limit=limit):
                result = search_youtube("test", limit=limit)

                self.assertEqual(
                    result,
                    {
                        "success": False,
                        "error": "Limit must be between 1 and 50.",
                    },
                )
        mock_get.assert_not_called()

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
    def test_reports_malformed_json_response(self, mock_get):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.side_effect = ValueError("invalid JSON")
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

    @patch("mcp.tools.httpx.get")
    def test_handles_non_json_api_error(self, mock_get):
        request = httpx.Request("GET", "https://example.test")
        response = Mock()
        response.json.side_effect = ValueError("invalid JSON")
        response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "server error",
            request=request,
            response=response,
        )
        mock_get.return_value = response

        result = search_youtube("test", limit=5)

        self.assertEqual(
            result,
            {
                "success": False,
                "error": "server error",
            },
        )

    @patch("mcp.tools.httpx.get")
    def test_reports_request_timeout(self, mock_get):
        request = httpx.Request("GET", "https://example.test")
        mock_get.side_effect = httpx.ReadTimeout("timed out", request=request)

        result = search_youtube("test", limit=5)

        self.assertEqual(
            result,
            {
                "success": False,
                "error": "YouTube API request timed out. Please try again.",
            },
        )

    @patch("mcp.tools.httpx.get")
    def test_reports_connection_error(self, mock_get):
        request = httpx.Request("GET", "https://example.test")
        mock_get.side_effect = httpx.ConnectError(
            "connection failed",
            request=request,
        )

        result = search_youtube("test", limit=5)

        self.assertEqual(
            result,
            {
                "success": False,
                "error": "connection failed",
            },
        )


if __name__ == "__main__":
    unittest.main()
