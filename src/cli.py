"""
Command-line interface for the database chatbot.
"""
import sys
import argparse

from .config import validate_config
from .agent import setup_agent
from .utils import Spinner


def chat_loop(agent_executor, verbose=False):
    """
    Run the interactive chat loop.
    
    Args:
        agent_executor: Initialized agent executor
        verbose (bool): Whether to show detailed operations
    """
    print("=" * 60)
    print("E-Commerce Database Chat CLI")
    print("=" * 60)
    print("Ask questions about your e-commerce data in natural language.")
    print("Type 'exit' or 'quit' to end the session.")
    if verbose:
        print("Verbose mode: ON - Showing background operations")
    print()
    
    while True:
        try:
            # Get user input
            question = input("\n🔍 Your question: ").strip()
            
            # Check for exit commands
            if question.lower() in ['exit', 'quit', 'q']:
                print("\nGoodbye!")
                break
            
            # Skip empty input
            if not question:
                continue
            
            # Process question with spinner (unless verbose mode)
            if not verbose:
                spinner = Spinner("Thinking")
                spinner.start()
            
            try:
                response = agent_executor.invoke({"input": question})
            finally:
                if not verbose:
                    spinner.stop()
            
            print(f"💡 Answer: {response['output']}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try rephrasing your question.")


def parse_args():
    """
    Parse command-line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Chat with your e-commerce database using natural language"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed background operations (SQL queries, agent reasoning)"
    )
    return parser.parse_args()


def main():
    """Main entry point for the CLI application."""
    args = parse_args()
    
    try:
        # Validate configuration
        validate_config()
        
        # Setup agent
        agent_executor = setup_agent(verbose=args.verbose)
        
        # Start chat loop
        chat_loop(agent_executor, verbose=args.verbose)
        
    except (ValueError, FileNotFoundError) as e:
        print(f"Configuration error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
