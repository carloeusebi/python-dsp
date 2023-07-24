import unittest
from unittest.mock import MagicMock, patch
from website.website import Website


class TestWebsite(unittest.TestCase):
    def setUp(self):
        self.url = "https://example.com/api"
        self.website = Website(self.url)
        assert self.url == self.website.url
        assert self.website.cookie == ""

    def _mock_response(
        self,
        status=200,
        content="CONTENT",
        json_data=None,
        raise_for_status=None,
        cookie=None,
    ):
        mock_resp = MagicMock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        mock_resp.status_code = status
        mock_resp.content = content
        mock_resp.cookies = cookie
        if json_data:
            mock_resp.json = MagicMock(return_value=json_data)
        return mock_resp

    def test_login_successful(self):
        mock_res = self._mock_response(
            json_data={"session_id": "12345"}, cookie={"TOKEN": "abcdef"}
        )
        with patch("requests.post", return_value=mock_res):
            credentials = {"username": "testuser", "password": "testpassword"}
            self.assertTrue(self.website.login(credentials))
            self.assertEqual(self.website.cookie, "TOKEN=abcdef; PHPSESSID=12345")


if __name__ == "main":
    unittest.main()
