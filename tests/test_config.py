"""Tests for configuration module."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest


def test_config_loads_env_vars(mock_env_vars, monkeypatch):
    """Test that configuration loads environment variables correctly."""
    # Ensure DB_PATH is set correctly
    monkeypatch.setenv("DB_PATH", "ecommerce.db")

    # Import after setting env vars
    import importlib

    from src import config

    importlib.reload(config)

    assert config.OPENAI_API_KEY == "sk-test-key-123"
    assert config.MODEL == "gpt-4o-mini"
    assert config.TEMPERATURE == 0.0
    assert config.DB_PATH == "ecommerce.db"


def test_config_uses_defaults(monkeypatch):
    """Test that configuration uses default values when env vars not set."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.delenv("MODEL", raising=False)
    monkeypatch.delenv("TEMPERATURE", raising=False)
    monkeypatch.delenv("DB_PATH", raising=False)

    # Reload config module to pick up changes
    import importlib

    from src import config

    importlib.reload(config)

    assert config.MODEL == "gpt-4o-mini"
    assert config.TEMPERATURE == 0.0
    assert config.DB_PATH == "ecommerce.db"


def test_validate_config_missing_api_key(tmp_path):
    """Test validation fails when API key is missing."""
    from src import config

    # Temporarily override the API key value and create a temp DB
    original_key = config.OPENAI_API_KEY
    fake_db = tmp_path / "test.db"
    fake_db.touch()
    original_db = config.DB_PATH

    try:
        config.OPENAI_API_KEY = None
        config.DB_PATH = str(fake_db)

        with pytest.raises(ValueError, match="Please set your OPENAI_API_KEY"):
            config.validate_config()
    finally:
        # Restore original values
        config.OPENAI_API_KEY = original_key
        config.DB_PATH = original_db


def test_validate_config_placeholder_api_key(mock_env_vars, monkeypatch):
    """Test validation fails when API key is placeholder."""
    monkeypatch.setenv("OPENAI_API_KEY", "your-api-key-here")

    import importlib

    from src import config

    importlib.reload(config)

    with pytest.raises(ValueError, match="Please set your OPENAI_API_KEY"):
        config.validate_config()


def test_validate_config_missing_database(mock_env_vars, monkeypatch, tmp_path):
    """Test validation fails when database doesn't exist."""
    fake_db = tmp_path / "nonexistent.db"
    monkeypatch.setenv("DB_PATH", str(fake_db))

    import importlib

    from src import config

    importlib.reload(config)

    with pytest.raises(FileNotFoundError, match="Database .* not found"):
        config.validate_config()


def test_validate_config_success(mock_env_vars, temp_db, monkeypatch):
    """Test validation succeeds with valid configuration."""
    monkeypatch.setenv("DB_PATH", temp_db)

    import importlib

    from src import config

    importlib.reload(config)

    # Should not raise
    config.validate_config()


def test_system_prompt_contains_filtering_rules():
    """Test that system prompt includes data filtering instructions."""
    from src.config import SYSTEM_PROMPT

    assert "filter" in SYSTEM_PROMPT.lower()
    assert "UnitPrice" in SYSTEM_PROMPT
    assert "adjustment" in SYSTEM_PROMPT.lower()
