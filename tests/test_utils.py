"""Tests for utility module."""

import time
import pytest
from io import StringIO
from unittest.mock import patch


def test_spinner_initialization():
    """Test Spinner class initializes correctly."""
    from src.utils import Spinner

    spinner = Spinner("Test")
    assert spinner.message == "Test"
    assert spinner.running is False
    assert spinner.thread is None


def test_spinner_default_message():
    """Test Spinner uses default message."""
    from src.utils import Spinner

    spinner = Spinner()
    assert spinner.message == "Processing"


def test_spinner_start_stop():
    """Test Spinner starts and stops correctly."""
    from src.utils import Spinner

    spinner = Spinner("Test")

    # Start spinner
    spinner.start()
    assert spinner.running is True
    assert spinner.thread is not None
    assert spinner.thread.is_alive()

    # Give it a moment to spin
    time.sleep(0.2)

    # Stop spinner
    spinner.stop()
    assert spinner.running is False

    # Wait for thread to finish
    time.sleep(0.1)
    assert not spinner.thread.is_alive()


def test_spinner_is_daemon_thread():
    """Test Spinner thread is daemon (won't block program exit)."""
    from src.utils import Spinner

    spinner = Spinner("Test")
    spinner.start()

    assert spinner.thread is not None
    assert spinner.thread.daemon is True

    spinner.stop()


def test_spinner_animation_output():
    """Test Spinner produces animation output."""
    from src.utils import Spinner

    spinner = Spinner("Loading")

    with patch("sys.stdout", new=StringIO()) as fake_out:
        spinner.start()
        time.sleep(0.25)  # Let it spin a few times
        spinner.stop()

        output = fake_out.getvalue()
        # Should have written to stdout (though cleared at end)
        assert len(output) > 0


def test_spinner_clears_line_on_stop():
    """Test Spinner clears its output line when stopped."""
    from src.utils import Spinner

    spinner = Spinner("Test message")

    with patch("sys.stdout", new=StringIO()) as fake_out:
        spinner.start()
        time.sleep(0.1)
        spinner.stop()

        output = fake_out.getvalue()
        # Should end with carriage return (line cleared)
        assert output.endswith("\r")


def test_spinner_multiple_start_stop_cycles():
    """Test Spinner can be started and stopped multiple times."""
    from src.utils import Spinner

    spinner = Spinner("Test")

    # First cycle
    spinner.start()
    time.sleep(0.1)
    spinner.stop()

    # Second cycle
    spinner.start()
    assert spinner.running is True
    time.sleep(0.1)
    spinner.stop()
    assert spinner.running is False
