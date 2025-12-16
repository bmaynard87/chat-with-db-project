"""Pytest configuration and shared fixtures."""

import os
import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set up mock environment variables for testing."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key-123")
    monkeypatch.setenv("MODEL", "gpt-4o-mini")
    monkeypatch.setenv("TEMPERATURE", "0")
    monkeypatch.setenv("DB_PATH", "ecommerce.db")
    yield


@pytest.fixture
def temp_db():
    """Create a temporary database file for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    # Create a simple database with test data
    import sqlite3

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE transactions (
            InvoiceNo TEXT,
            StockCode TEXT,
            Description TEXT,
            Quantity INTEGER,
            InvoiceDate TEXT,
            UnitPrice REAL,
            CustomerID REAL,
            Country TEXT
        )
    """
    )
    cursor.execute(
        """
        INSERT INTO transactions VALUES
        ('123', 'A001', 'Test Product', 5, '2024-01-01', 10.0, 1001.0, 'USA'),
        ('124', 'A002', 'Another Product', 3, '2024-01-02', 15.0, 1002.0, 'UK'),
        ('125', 'ADJ', 'Adjustment', 1, '2024-01-03', -5.0, 1003.0, 'USA')
    """
    )
    conn.commit()
    conn.close()

    yield db_path

    # Cleanup
    os.unlink(db_path)


@pytest.fixture
def mock_agent():
    """Create a mock agent executor for testing."""
    agent = Mock()
    agent.invoke.return_value = {"output": "Test response"}
    return agent


@pytest.fixture
def mock_openai():
    """Mock OpenAI API calls."""
    with patch("src.agent.ChatOpenAI") as mock:
        mock.return_value = Mock()
        yield mock


@pytest.fixture
def mock_sql_agent():
    """Mock SQL agent creation."""
    with patch("src.agent.create_sql_agent") as mock:
        agent = Mock()
        agent.invoke.return_value = {"output": "Test response"}
        mock.return_value = agent
        yield mock
