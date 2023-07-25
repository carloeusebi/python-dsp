import unittest
from unittest.mock import MagicMock, patch
from requests.exceptions import HTTPError
from io import StringIO

from website.website import Website


class TestWebsite(unittest.TestCase):
    def setUp(self):
        self.url = "https://example.com/api"
        self.website = Website(self.url)
        self.credentials = {"username": "testuser", "password": "testpassword"}
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
            self.assertTrue(self.website.login(self.credentials))
            self.assertEqual(self.website.cookie, "TOKEN=abcdef; PHPSESSID=12345")

    @patch("sys.stdout", new_callable=StringIO)
    def test_login_wrong_credentials(self, stdout):
        mock_res = self._mock_response(
            raise_for_status=HTTPError("invalid-credentials"), status=401
        )
        expected_out = "Login in corso...\nUsername o Password non validi\n"
        with patch("requests.post", return_value=mock_res):
            self.assertFalse(self.website.login(self.credentials))
            self.assertEqual(stdout.getvalue(), expected_out)

    @patch("website.website.utils", MagicMock())
    @patch("sys.stdout", new_callable=StringIO)
    def test_login_server_error(self, stdout):
        mock_res = self._mock_response(raise_for_status=HTTPError(""), status=500)
        expected_out = "Login in corso...\nC'è stato un problema con il server, Riprovare più tardi\n"
        with patch("requests.post", return_value=mock_res):
            self.assertFalse(self.website.login(self.credentials))
            self.assertEqual(stdout.getvalue(), expected_out)

    def test_get_success(self):
        json_data = {
            "labels": ["id", "Nome", "Cognome"],
            "list": [
                {"id": 1, "fname": "Carlo", "lname": "Eusebi"},
                {"id": 2, "fname": "Susan", "lname": "Brardinelli"},
            ],
        }
        mock_res = self._mock_response(json_data=json_data)
        with patch("requests.get", return_value=mock_res):
            response = self.website.get("endpoint", "id")
            assert response == json_data["list"]

    @patch("website.website.utils", MagicMock())
    @patch("sys.stdout", new_callable=StringIO)
    def test_get_server_error(self, stdout):
        mock_res = self._mock_response(
            raise_for_status=HTTPError("Error 500"), status=500
        )
        expected_out = "C'è stato un problema con il server, Riprovare più tardi\n"
        with patch("requests.get", return_value=mock_res):
            response = self.website.get("endpoint", "id")
            self.assertEqual(response, None)
            self.assertEqual(stdout.getvalue(), expected_out)
