"""Tests for memory module."""

import pytest
from langchain_core.messages import HumanMessage, AIMessage


def test_memory_initialization():
    """Test that memory can be initialized."""
    from src.memory import create_memory
    
    memory = create_memory("test_session_1")
    assert memory is not None
    assert hasattr(memory, "messages")


def test_memory_stores_conversation():
    """Test that memory stores messages."""
    from src.memory import create_memory
    
    memory = create_memory("test_session_2")
    memory.add_user_message("What is the total revenue?")
    memory.add_ai_message("$1000")
    
    # Verify memory has stored the conversation
    messages = memory.messages
    assert len(messages) == 2
    assert isinstance(messages[0], HumanMessage)
    assert isinstance(messages[1], AIMessage)


def test_memory_retrieves_history():
    """Test that memory can retrieve chat history."""
    from src.memory import create_memory, get_session_history
    
    memory = create_memory("test_session_3")
    memory.add_user_message("Question 1")
    memory.add_ai_message("Answer 1")
    memory.add_user_message("Question 2")
    memory.add_ai_message("Answer 2")
    
    # Retrieve the same session
    retrieved = get_session_history("test_session_3")
    assert len(retrieved.messages) == 4
    assert retrieved.messages[0].content == "Question 1"


def test_memory_clear():
    """Test that memory can be cleared."""
    from src.memory import create_memory, clear_memory
    
    memory = create_memory("test_session_4")
    memory.add_user_message("Question")
    memory.add_ai_message("Answer")
    
    # Clear memory
    clear_memory("test_session_4")
    
    # Get a new session (old one should be gone)
    new_memory = create_memory("test_session_4")
    assert len(new_memory.messages) == 0


def test_memory_session_isolation():
    """Test that different sessions have isolated memory."""
    from src.memory import create_memory
    
    session1 = create_memory("session_a")
    session2 = create_memory("session_b")
    
    session1.add_user_message("Message for session A")
    session2.add_user_message("Message for session B")
    
    assert len(session1.messages) == 1
    assert len(session2.messages) == 1
    assert session1.messages[0].content != session2.messages[0].content
