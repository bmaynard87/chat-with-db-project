"""Tests for CLI module."""

import pytest
import sys
from io import StringIO
from unittest.mock import Mock, patch, call


def test_parse_args_default():
    """Test argument parsing with no flags."""
    from src.cli import parse_args

    with patch("sys.argv", ["chat_cli.py"]):
        args = parse_args()
        assert args.verbose is False


def test_parse_args_verbose_flag():
    """Test argument parsing with verbose flag."""
    from src.cli import parse_args

    with patch("sys.argv", ["chat_cli.py", "-v"]):
        args = parse_args()
        assert args.verbose is True

    with patch("sys.argv", ["chat_cli.py", "--verbose"]):
        args = parse_args()
        assert args.verbose is True


def test_chat_loop_exit_commands(mock_agent, capsys):
    """Test chat loop exits on exit commands."""
    from src.cli import chat_loop

    # Test 'exit'
    with patch("builtins.input", side_effect=["exit"]):
        chat_loop(mock_agent)
        captured = capsys.readouterr()
        assert "Goodbye" in captured.out

    # Test 'quit'
    with patch("builtins.input", side_effect=["quit"]):
        chat_loop(mock_agent)
        captured = capsys.readouterr()
        assert "Goodbye" in captured.out


def test_chat_loop_processes_question(mock_agent, capsys):
    """Test chat loop processes valid questions."""
    from src.cli import chat_loop

    with patch("builtins.input", side_effect=["What is the revenue?", "exit"]):
        chat_loop(mock_agent, verbose=True)  # verbose=True to skip spinner

        mock_agent.invoke.assert_called_once_with({"input": "What is the revenue?"})
        captured = capsys.readouterr()
        assert "Test response" in captured.out


def test_chat_loop_handles_empty_input(mock_agent):
    """Test chat loop skips empty input."""
    from src.cli import chat_loop

    with patch("builtins.input", side_effect=["", "  ", "exit"]):
        chat_loop(mock_agent, verbose=True)

        # Should not invoke agent for empty inputs
        assert mock_agent.invoke.call_count == 0


def test_chat_loop_handles_keyboard_interrupt(mock_agent, capsys):
    """Test chat loop handles Ctrl+C gracefully."""
    from src.cli import chat_loop

    with patch("builtins.input", side_effect=KeyboardInterrupt()):
        chat_loop(mock_agent)
        captured = capsys.readouterr()
        assert "Goodbye" in captured.out


def test_chat_loop_handles_agent_errors(mock_agent, capsys):
    """Test chat loop handles agent errors gracefully."""
    from src.cli import chat_loop

    mock_agent.invoke.side_effect = Exception("Test error")

    with patch("builtins.input", side_effect=["test question", "exit"]):
        chat_loop(mock_agent, verbose=True)
        captured = capsys.readouterr()
        assert "Error" in captured.out
        assert "Test error" in captured.out


def test_chat_loop_verbose_mode(mock_agent, capsys):
    """Test chat loop shows verbose indicator."""
    from src.cli import chat_loop

    with patch("builtins.input", side_effect=["exit"]):
        chat_loop(mock_agent, verbose=True)
        captured = capsys.readouterr()
        assert "Verbose mode: ON" in captured.out


def test_main_validates_config(mock_env_vars, mock_agent):
    """Test main function validates configuration."""
    from src.cli import main

    with (
        patch("src.cli.validate_config") as mock_validate,
        patch("src.cli.setup_agent", return_value=mock_agent),
        patch("src.cli.chat_loop"),
        patch("src.cli.parse_args", return_value=Mock(verbose=False)),
    ):

        main()
        mock_validate.assert_called_once()


def test_main_handles_config_errors(mock_env_vars):
    """Test main exits on configuration errors."""
    from src.cli import main

    with (
        patch("src.cli.validate_config", side_effect=ValueError("Config error")),
        patch("src.cli.parse_args", return_value=Mock(verbose=False)),
        pytest.raises(SystemExit) as exc_info,
    ):

        main()
        assert exc_info.value.code == 1


def test_main_handles_fatal_errors(mock_env_vars, mock_agent):
    """Test main handles unexpected errors."""
    from src.cli import main

    with (
        patch("src.cli.validate_config"),
        patch("src.cli.setup_agent", side_effect=Exception("Fatal error")),
        patch("src.cli.parse_args", return_value=Mock(verbose=False)),
        pytest.raises(SystemExit) as exc_info,
    ):

        main()
        assert exc_info.value.code == 1
