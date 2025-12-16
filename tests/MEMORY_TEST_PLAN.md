"""Test plan for conversation memory feature.

Test scenarios to implement:

1. Memory Module Tests (tests/test_memory.py)
   - test_memory_initialization: Verify ConversationBufferMemory creates correctly
   - test_memory_stores_conversation: Check messages are stored in memory
   - test_memory_retrieves_history: Verify chat history can be retrieved
   - test_memory_clear: Test clearing memory resets history
   - test_memory_context_window: Test memory limits if using windowed memory

2. Agent Integration Tests (tests/test_agent.py)
   - test_agent_with_memory: Agent initializes with memory
   - test_agent_uses_memory: Agent accesses conversation history
   - test_memory_passed_to_agent: Memory object correctly passed to agent executor

3. CLI Integration Tests (tests/test_cli.py)
   - test_chat_loop_maintains_memory: Memory persists across questions in session
   - test_follow_up_question: Agent understands context from previous question
   - test_memory_cleared_on_exit: Memory resets when chat loop exits
   - test_memory_in_verbose_mode: Memory works with verbose flag

4. End-to-End Memory Tests (tests/test_integration.py)
   - test_conversation_flow_with_context: Full conversation with follow-ups
   - test_pronoun_resolution: Agent resolves "it", "them", "that" from context
   - test_comparative_queries: "What about X?" after asking about Y
   - test_memory_overflow: Handles long conversations gracefully

Implementation approach:
- Create src/memory.py with memory setup utilities
- Update src/agent.py to accept and use memory
- Update src/cli.py to create and pass memory to agent
- Mock LLM responses in tests to verify memory integration
- Test both unit (isolated memory) and integration (full flow) scenarios
"""
