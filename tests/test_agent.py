"""Tests for agent module."""

from unittest.mock import MagicMock, Mock, patch

import pytest


def test_setup_agent_creates_database_connection(mock_env_vars, mock_openai, mock_sql_agent, temp_db, monkeypatch):
    """Test that setup_agent creates database connection."""
    monkeypatch.setenv("DB_PATH", temp_db)

    import importlib

    from src import agent, config

    importlib.reload(config)

    with patch("src.agent.SQLDatabase") as mock_db, patch("src.agent.SQLDatabaseToolkit") as mock_toolkit:
        mock_db.from_uri.return_value = Mock()
        mock_toolkit.return_value = Mock()
        agent.setup_agent()

        mock_db.from_uri.assert_called_once()
        call_args = mock_db.from_uri.call_args[0][0]
        assert "sqlite:///" in call_args


def test_setup_agent_initializes_llm(mock_env_vars, mock_openai, mock_sql_agent):
    """Test that setup_agent initializes LLM with correct parameters."""
    from src import agent

    with patch("src.agent.SQLDatabase"), patch("src.agent.SQLDatabaseToolkit"):
        agent.setup_agent()

        mock_openai.assert_called_once()
        call_kwargs = mock_openai.call_args[1]
        assert call_kwargs["model"] == "gpt-4o-mini"
        assert call_kwargs["temperature"] == 0.0


def test_setup_agent_creates_sql_agent(mock_env_vars, mock_openai, mock_sql_agent):
    """Test that setup_agent creates SQL agent with toolkit."""
    from src import agent

    with patch("src.agent.SQLDatabase"), patch("src.agent.SQLDatabaseToolkit") as mock_toolkit:

        agent.setup_agent()

        mock_toolkit.assert_called_once()
        mock_sql_agent.assert_called_once()


def test_setup_agent_verbose_mode(mock_env_vars, mock_openai, mock_sql_agent):
    """Test that verbose flag is passed to agent."""
    from src import agent

    with patch("src.agent.SQLDatabase"), patch("src.agent.SQLDatabaseToolkit"):

        agent.setup_agent(verbose=True)

        call_kwargs = mock_sql_agent.call_args[1]
        assert call_kwargs["verbose"] is True


def test_setup_agent_includes_system_prompt(mock_env_vars, mock_openai, mock_sql_agent):
    """Test that system prompt is included in agent configuration."""
    from src import agent
    from src.config import SYSTEM_PROMPT

    with patch("src.agent.SQLDatabase"), patch("src.agent.SQLDatabaseToolkit"):

        agent.setup_agent()

        call_kwargs = mock_sql_agent.call_args[1]
        assert "agent_executor_kwargs" in call_kwargs
        assert call_kwargs["agent_executor_kwargs"]["system_message"] == SYSTEM_PROMPT


def test_setup_agent_uses_openai_tools_type(mock_env_vars, mock_openai, mock_sql_agent):
    """Test that agent uses openai-tools agent type."""
    from src import agent

    with patch("src.agent.SQLDatabase"), patch("src.agent.SQLDatabaseToolkit"):

        agent.setup_agent()

        call_kwargs = mock_sql_agent.call_args[1]
        assert call_kwargs["agent_type"] == "openai-tools"
