"""
Conversation memory management for the chatbot.
"""

from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory

# Session-scoped message history store
_store: dict[str, BaseChatMessageHistory] = {}


def get_session_history(session_id: str = "default") -> BaseChatMessageHistory:
    """
    Get or create a chat message history for a session.

    Args:
        session_id: Unique identifier for the conversation session

    Returns:
        BaseChatMessageHistory instance for the session
    """
    if session_id not in _store:
        _store[session_id] = InMemoryChatMessageHistory()
    return _store[session_id]


def create_memory(session_id: str = "default") -> BaseChatMessageHistory:
    """
    Create a conversation memory instance for the agent.

    Args:
        session_id: Unique identifier for the conversation session

    Returns:
        BaseChatMessageHistory instance configured for the SQL agent
    """
    return get_session_history(session_id)


def clear_memory(session_id: str = "default") -> None:
    """
    Clear the conversation history for a session.

    Args:
        session_id: Unique identifier for the conversation session
    """
    if session_id in _store:
        _store[session_id].clear()
        del _store[session_id]
