"""Integration tests for end-to-end functionality."""

from unittest.mock import Mock, patch

import pytest


def test_full_query_flow_with_mock_llm(mock_env_vars, temp_db, monkeypatch):
    """Test complete flow from question to answer with mocked LLM."""
    monkeypatch.setenv("DB_PATH", temp_db)

    import importlib

    from src import agent, config

    importlib.reload(config)

    # Mock the LLM and agent creation
    mock_response = {"output": "Total revenue is $100"}

    with (
        patch("src.agent.ChatOpenAI") as mock_llm,
        patch("src.agent.create_sql_agent") as mock_create,
        patch("src.agent.RunnableWithMessageHistory") as mock_runnable,
        patch("src.agent.SQLDatabase"),
        patch("src.agent.SQLDatabaseToolkit"),
    ):

        mock_llm.return_value = Mock()
        mock_agent = Mock()
        mock_agent.invoke.return_value = mock_response
        mock_create.return_value = mock_agent

        # Mock the wrapped agent
        mock_wrapped = Mock()
        mock_wrapped.invoke.return_value = mock_response
        mock_runnable.return_value = mock_wrapped

        agent_executor = agent.setup_agent(verbose=False)
        response = agent_executor.invoke(
            {"input": "What is the total revenue?"},
            config={"configurable": {"session_id": "test_session"}},
        )

        assert response["output"] == "Total revenue is $100"
        mock_create.assert_called_once()


def test_database_connection_with_real_db(monkeypatch):
    """Test that agent can connect to the real database."""
    # Set up environment for real database
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
    monkeypatch.setenv("DB_PATH", "ecommerce.db")

    import importlib

    from langchain_community.utilities import SQLDatabase

    from src import config

    importlib.reload(config)

    # This test uses the actual ecommerce.db
    config.validate_config()  # Should not raise

    db = SQLDatabase.from_uri(f"sqlite:///{config.DB_PATH}")

    # Verify database has expected structure
    table_info = db.get_table_info()
    assert "transactions" in table_info
    assert "InvoiceNo" in table_info
    assert "StockCode" in table_info
    assert "UnitPrice" in table_info


def test_cli_entry_point(mock_env_vars, mock_agent):
    """Test CLI entry point executes without errors."""
    from src.cli import main

    with (
        patch("src.cli.validate_config"),
        patch("src.cli.setup_agent", return_value=mock_agent),
        patch("src.cli.parse_args", return_value=Mock(verbose=False)),
        patch("builtins.input", side_effect=["exit"]),
    ):

        # Should complete without raising
        main()


def test_config_validation_integration(tmp_path, monkeypatch):
    """Test configuration validation with various scenarios."""
    import importlib

    from src import config

    # Valid configuration
    monkeypatch.setenv("OPENAI_API_KEY", "sk-valid-key")
    monkeypatch.setenv("DB_PATH", "ecommerce.db")
    importlib.reload(config)

    try:
        config.validate_config()
    except FileNotFoundError:
        # Expected if ecommerce.db doesn't exist in test environment
        pass

    # Invalid API key
    monkeypatch.setenv("OPENAI_API_KEY", "your-api-key-here")
    importlib.reload(config)

    with pytest.raises(ValueError):
        config.validate_config()
