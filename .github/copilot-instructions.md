# Copilot Instructions: E-Commerce Database Chat

## Project Overview
RAG-enabled natural language chatbot for querying e-commerce data using LangChain SQL agents. Users interact via CLI or notebook interface to ask questions about transactions, products, and revenue in plain English.

## Architecture

### Core Components
- **Entry Point**: [chat_cli.py](../chat_cli.py) → delegates to `src.cli.main()`
- **Agent Layer**: [src/agent.py](../src/agent.py) - LangChain SQL agent using `openai-tools` agent type
- **Memory Layer**: [src/memory.py](../src/memory.py) - Conversation memory for context-aware queries
- **CLI Interface**: [src/cli.py](../src/cli.py) - interactive chat loop with optional verbose mode
- **Config**: [src/config.py](../src/config.py) - centralized settings with `.env` integration
- **Utils**: [src/utils.py](../src/utils.py) - `Spinner` class for non-verbose UI feedback

### Data Flow
1. User enters natural language question
2. CLI passes question + conversation history to LangChain SQL agent
3. Agent uses conversation memory for context understanding
4. Agent uses `SQLDatabaseToolkit` to query SQLite database (`ecommerce.db`)
5. Response formatted and returned through CLI
6. Conversation memory updated with question and answer

## Critical Setup Requirements

**Environment Variables** (`.env` file required):
```bash
OPENAI_API_KEY=sk-...  # Must be valid, not "your-api-key-here"
MODEL=gpt-4o-mini       # Optional, defaults to gpt-4o-mini
TEMPERATURE=0           # Optional, defaults to 0
DB_PATH=ecommerce.db    # Optional, defaults to ecommerce.db
```

**Database**: `ecommerce.db` (536K+ rows, included in repo)
- **Schema**: Single `transactions` table with columns:
  - `InvoiceNo` (TEXT) - Transaction identifier
  - `StockCode` (TEXT) - Product SKU
  - `Description` (TEXT) - Product/entry description
  - `Quantity` (INTEGER) - Items purchased
  - `InvoiceDate` (TEXT) - Transaction timestamp
  - `UnitPrice` (REAL) - Price per unit
  - `CustomerID` (REAL) - Customer identifier
  - `Country` (TEXT) - Customer country
- Real e-commerce transaction data from an online retailer

## Developer Workflows

### Running the CLI
```bash
# Standard mode (with spinner)
python chat_cli.py

# Verbose mode (shows SQL queries and agent reasoning)
python chat_cli.py -v
```

### Testing Configuration
The CLI validates config on startup via `validate_config()`:
- Checks for valid `OPENAI_API_KEY` (not placeholder)
- Verifies `ecommerce.db` exists
- Exits with clear error messages if validation fails

## Project-Specific Conventions

### Data Filtering Pattern (CRITICAL)
The agent has domain-specific filtering logic in `SYSTEM_PROMPT` (see [src/config.py](../src/config.py#L17-L25)):
- **Exclude non-product entries**: adjustments, bad debt, postage, fees (check `Description` field)
- **Filter invalid prices**: `UnitPrice <= 0` excluded from product/revenue queries
- **Why this matters**: The transactions table mixes actual product sales with accounting adjustments
- This is the "business logic" layer - embedded in the LLM prompt rather than SQL views

### Error Handling
- Configuration errors (missing API key, no DB) exit immediately with `sys.exit(1)`
- Runtime errors (query failures) caught in chat loop, prompt user to rephrase
- `KeyboardInterrupt` handled gracefully for clean exits

### Agent Configuration
Agent uses:
- **Agent Type**: `openai-tools` (leverages OpenAI function calling)
- **Temperature**: 0 (deterministic responses for queries)
- **System Prompt**: Embedded domain knowledge about filtering e-commerce data
- **Memory**: `ConversationBufferMemory` for maintaining chat context
- **Verbose Mode**: Controlled via CLI flag, passed through to agent

### Memory Implementation
Conversation memory enables context-aware queries:
- **Type**: `ConversationBufferMemory` from LangChain
- **Scope**: Per-session (cleared on exit)
- **Usage**: Agent can reference previous questions/answers
- **Benefits**: Follow-up questions ("What about X?", "Show me more", "How does that compare?")
- **Memory Key**: `chat_history` passed to agent executor

## Dependencies & Tech Stack
- **LangChain**: SQL agent framework (`langchain-community`, `langchain-openai`)
- **Database**: SQLite via `langchain_community.utilities.SQLDatabase`
- **LLM**: OpenAI ChatGPT (configurable model via `.env`)
- **UI**: Terminal-based with custom `Spinner` class (threading-based)

## Testing Approach
Comprehensive test suite with **35 tests** and **96% code coverage**:
- **Unit Tests**: [tests/test_config.py](../tests/test_config.py), [tests/test_agent.py](../tests/test_agent.py), [tests/test_cli.py](../tests/test_cli.py), [tests/test_utils.py](../tests/test_utils.py)
- **Integration Tests**: [tests/test_integration.py](../tests/test_integration.py)
- **Fixtures**: [tests/conftest.py](../tests/conftest.py) - Shared mocks for env vars, databases, and agents

All OpenAI API calls are mocked in tests (no API charges). Run with: `pytest` or `pytest --cov=src`

### CI/CD Pipeline
GitHub Actions workflows in [.github/workflows/](../..github/workflows/):
- **CI**: Tests on Python 3.9-3.12 × (Ubuntu, Windows, macOS) with linting (flake8, black, isort, mypy)
- **Release**: Automated package building via [pyproject.toml](../pyproject.toml)
- Code quality tools configured in [.flake8](../.flake8) and pyproject.toml

## Key Files to Reference
- [src/config.py](../src/config.py) - Contains `SYSTEM_PROMPT` with data filtering rules
- [src/agent.py](../src/agent.py) - Single-function module, shows LangChain agent setup pattern
- [src/cli.py](../src/cli.py#L10-L58) - `chat_loop()` demonstrates conversation flow and error handling
- [requirements.txt](../requirements.txt) - Minimal dependencies (pandas, langchain stack, dotenv)
