from io import StringIO
from unittest.mock import MagicMock, patch

from utils import utils


def test_clearscreen():
    # just test that it doesn't raise any errors
    utils.clearscreen()


@patch("builtins.input", MagicMock())
@patch("builtins.exit", MagicMock())
@patch("sys.stdout", new_callable=StringIO)
def test_die(stdout):
    output = "test error"
    expected_out = f"{output}"
    # test die without param
    utils.die()
    assert stdout.getvalue() == ""
    # test die with param
    utils.die(output)
    assert stdout.getvalue() == expected_out + "\n"


def test_test_passed():
    assert utils.test_passed() == False
