"""
Utility functions and classes.
"""
import sys
import threading
import time


class Spinner:
    """Simple spinner for showing progress during processing."""
    
    def __init__(self, message="Processing"):
        """
        Initialize the spinner.
        
        Args:
            message (str): Message to display next to spinner
        """
        self.message = message
        self.running = False
        self.thread = None
        
    def start(self):
        """Start the spinner animation."""
        self.running = True
        self.thread = threading.Thread(target=self._spin)
        self.thread.daemon = True
        self.thread.start()
        
    def stop(self):
        """Stop the spinner and clear the line."""
        self.running = False
        if self.thread:
            self.thread.join()
        sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')
        sys.stdout.flush()
        
    def _spin(self):
        """Run the spinner animation loop."""
        spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        idx = 0
        while self.running:
            sys.stdout.write(f'\r{spinner_chars[idx]} {self.message}...')
            sys.stdout.flush()
            idx = (idx + 1) % len(spinner_chars)
            time.sleep(0.1)
