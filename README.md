# E-Commerce Database Chat

> **Note:** This is a demonstration project showcasing RAG-enabled natural language database querying.

A RAG-enabled chatbot that lets you query e-commerce data using natural language. Built with LangChain SQL agents and OpenAI, it enables intuitive queries against 536,000+ real transaction records.

[![CI](https://github.com/YOUR_USERNAME/chat-with-db-project/workflows/CI/badge.svg)](https://github.com/YOUR_USERNAME/chat-with-db-project/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your OpenAI API key:
   - Copy `.env.example` to `.env` (or create `.env` file)
   - Replace `your-api-key-here` with your actual OpenAI API key

> **Note:** The database (`ecommerce.db`) is included in the repository, so no additional setup is required.

## Usage

Run the command-line chat interface:
```bash
python chat_cli.py
```

For verbose mode (shows SQL queries and agent reasoning):
```bash
python chat_cli.py -v
```

Then ask questions like:
- "What are the top 5 countries by total revenue?"
- "Show me the most popular products"
- "What is the average transaction value?"
- "How many transactions were there in December?"

Type `exit` or `quit` to end the session.

## Project Structure

- `chat_cli.py` - CLI entry point
- `src/` - Main application package
  - `cli.py` - Interactive chat loop and argument parsing
  - `agent.py` - LangChain SQL agent setup
  - `config.py` - Configuration and environment variables
  - `utils.py` - Helper utilities (Spinner class)
- `tests/` - Test suite (35 tests, 96% coverage)
  - `conftest.py` - Pytest fixtures and shared test utilities
  - `test_*.py` - Unit and integration tests
- `.github/workflows/` - CI/CD automation
  - `ci.yml` - Testing and linting pipeline
  - `release.yml` - Package build automation
- `ecommerce.db` - SQLite database (536K+ rows, included in repo)
- `.env` - Environment variables (API keys)
- `pyproject.toml` - Project configuration and dependencies
- `requirements.txt` - Python dependencies

## Database Schema

The `transactions` table contains:
- **InvoiceNo** - Transaction identifier
- **StockCode** - Product SKU
- **Description** - Product/entry description
- **Quantity** - Items purchased
- **InvoiceDate** - Transaction timestamp
- **UnitPrice** - Price per unit
- **CustomerID** - Customer identifier
- **Country** - Customer country

## Features

- 🤖 **Natural Language Queries**: Ask questions in plain English, get accurate answers
- 🔍 **Smart Data Filtering**: Automatically excludes non-product entries (adjustments, fees, etc.)
- 🎯 **High Accuracy**: 96% test coverage ensures reliable query results
- ⚡ **Fast Setup**: Database included, no data prep needed
- 🐛 **Debug Mode**: Verbose flag shows SQL queries and agent reasoning
- 🧪 **Well-Tested**: 35 automated tests across unit, integration, and CLI scenarios
- 🔄 **CI/CD Ready**: GitHub Actions pipeline with multi-platform testing

## How It Works

1. User enters a natural language question
2. LangChain SQL agent (using OpenAI's function calling) converts it to SQL
3. Query executes against the SQLite database
4. Agent formats and returns the answer in natural language

The agent includes domain-specific logic to filter out non-product entries (adjustments, bad debt, postage) for accurate product and revenue queries.

## Development

### Running Tests

Run the test suite with pytest:
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_config.py

# Run with verbose output
pytest -v
```

The test suite includes:
- **Unit tests** - Individual module testing with mocks
- **Integration tests** - End-to-end flow validation
- **Configuration tests** - Environment and setup validation
- **CLI tests** - Argument parsing and interactive loop testing

### Project Dependencies

Development dependencies are included in `requirements.txt`:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `pytest-mock` - Enhanced mocking support

Install development dependencies:
```bash
pip install -r requirements.txt
pip install flake8 black isort mypy
```

### Code Quality

Format code with black:
```bash
black src/ tests/
```

Sort imports with isort:
```bash
isort src/ tests/
```

Run linter:
```bash
flake8 src/
```

Type checking:
```bash
mypy src/ --ignore-missing-imports
```
