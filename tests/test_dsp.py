import unittest
from unittest.mock import patch

from dsp.dsp import get_credentials


class TestDsp(unittest.TestCase):
    @patch("dsp.dsp.prompt")
    def test_get_credentials(self, mocked_prompt):
        mocked_prompt.return_value = {"username": "test_user", "password": "test_pass"}
        result = get_credentials()
        self.assertIsInstance(result, dict)
        self.assertIn("username", result)
        self.assertIn("password", result)
        self.assertEqual(result["username"], "test_user")
        self.assertEqual(result["password"], "test_pass")
