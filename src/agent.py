"""
Agent setup and initialization.
"""

from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI

from .config import DB_PATH, MODEL, SYSTEM_PROMPT, TEMPERATURE


def setup_agent(verbose=False):
    """
    Initialize the SQL agent with database connection.

    Args:
        verbose (bool): Whether to show detailed agent operations

    Returns:
        Agent executor instance
    """
    # Connect to database
    db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")

    # Initialize LLM
    llm = ChatOpenAI(model=MODEL, temperature=TEMPERATURE)

    # Create agent with verbose setting and system prompt
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=SQLDatabaseToolkit(db=db, llm=llm),
        verbose=verbose,
        agent_type="openai-tools",
        agent_executor_kwargs={"system_message": SYSTEM_PROMPT},
    )

    return agent_executor
