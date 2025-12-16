"""
Agent setup and initialization.
"""

from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from .config import DB_PATH, MODEL, SYSTEM_PROMPT, TEMPERATURE
from .memory import get_session_history


def setup_agent(verbose=False, use_memory=True):
    """
    Initialize the SQL agent with database connection.

    Args:
        verbose (bool): Whether to show detailed agent operations
        use_memory (bool): Whether to enable conversation memory

    Returns:
        Agent executor instance (with memory if enabled)
    """
    # Connect to database
    db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")

    # Initialize LLM
    llm = ChatOpenAI(model=MODEL, temperature=TEMPERATURE)

    # Create prompt template with chat history support
    prompt_with_history = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    # Create agent with custom prompt that includes chat history
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=SQLDatabaseToolkit(db=db, llm=llm),
        verbose=verbose,
        agent_type="openai-tools",
        prompt=prompt_with_history,
    )

    # Wrap with memory if enabled
    if use_memory:
        agent_with_memory = RunnableWithMessageHistory(
            agent_executor,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )
        return agent_with_memory

    return agent_executor
