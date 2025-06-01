"""
Algorithm debugger and visualizer for step-by-step algorithm execution.
This module provides a core debugging infrastructure with visualization capabilities.
"""

import inspect
import bdb
import time

# Import utilities for visualization - fixed relative import
from .visualizer_utils import (
    is_two_pointer_algorithm, is_sorting_algorithm, 
    detect_array_and_pointers, detect_sorting_algorithm_state,
    simple_visualize, TerminalVisualizer
)

class DebugFrame:
    """Data structure to hold debug information for a single step."""
    
    def __init__(self, func_name, current_line, source_lines, start_line, variables, return_value=None, exception=None):
        self.func_name = func_name
        self.current_line = current_line
        self.source_lines = source_lines
        self.start_line = start_line
        self.variables = variables
        self.return_value = return_value
        self.exception = exception


class LineDebugger(bdb.Bdb):
    """
    A line-by-line code executor that captures execution state
    using Python's built-in debugging framework.
    """
    
    def __init__(self):
        super().__init__()
        self.locals = {}  # For storing local variables
        self.stop_execution = False
        self.current_frame = None
        self.current_line = 0
        self.source_lines = []
        self.source_filename = ""
        self.func_name = ""
        self.start_line = 0
        
        # List to store all debug frames
        self.debug_frames = []
        self.return_value = None
        self.exception = None
        
    def user_line(self, frame):
        """Called when a line is about to be executed."""
        if self.stop_execution:
            return
            
        # Track the current frame for variable inspection
        self.current_frame = frame
        self.current_line = frame.f_lineno
        
        # Extract local variables, filtering out internal variables
        filtered_locals = {}
        for name, value in frame.f_locals.items():
            if not name.startswith('_'):  # Skip internal variables
                try:
                    filtered_locals[name] = repr(value)
                except:
                    filtered_locals[name] = "<unprintable value>"
        
        # Create and store a debug frame
        debug_frame = DebugFrame(
            func_name=self.func_name,
            current_line=self.current_line,
            source_lines=self.source_lines,
            start_line=self.start_line,
            variables=filtered_locals
        )
        
        self.debug_frames.append(debug_frame)
        
    def user_return(self, frame, return_value):
        """Called when a function is about to return."""
        if self.stop_execution:
            return
        
        self.return_value = return_value
        
        # Add the return value to the last debug frame
        if self.debug_frames:
            self.debug_frames[-1].return_value = return_value
        
    def user_exception(self, frame, exc_info):
        """Called when an exception occurs."""
        exc_type, exc_value, exc_tb = exc_info
        self.exception = (exc_type.__name__, str(exc_value))
        
        # Add the exception to the last debug frame
        if self.debug_frames:
            self.debug_frames[-1].exception = self.exception
            
        self.stop_execution = True
        
    def run_function(self, func, source_code=None, start_line=2, *args, **kwargs):
        """
        Run a function line by line, capturing execution state at each step.
        Returns the result of the function and captured debug frames.
        """
        try:
            # Get the source code and line number of the function
            try:
                self.source_lines, self.start_line = inspect.getsourcelines(func)
                self.source_filename = inspect.getfile(func)
            except (OSError, IOError) as e:
                print('here amineh si ', e)
                # Handle dynamically created functions or other cases where inspect fails
                if source_code is not None:
                    # Split by newlines and handle different line endings
                    self.source_lines = source_code.strip().splitlines()
                    self.start_line = start_line
                    self.source_filename = "<dynamic>"
                else:
                    # If no source code is provided, create a placeholder
                    self.source_lines = ["<source code not available>"]
                    self.start_line = 1
                    self.source_filename = "<dynamic>"
            
            self.func_name = func.__name__
            
            # Clear previous debug frames
            self.debug_frames = []
            self.return_value = None
            self.exception = None
            
            # Reset debugger state
            self.stop_execution = False
            
            # Run the function under the debugger
            result = self.runcall(func, *args, **kwargs)
            
            # Return the result and all debug frames
            return result, {
                'function_name': self.func_name,
                'source_lines': self.source_lines,
                'start_line': self.start_line,
                'source_file': self.source_filename,
                'debug_frames': self.debug_frames,
                'args': args,
                'kwargs': kwargs,
                'return_value': self.return_value,
                'exception': self.exception
            }
            
        except KeyboardInterrupt:
            self.stop_execution = True
            return None, {
                'function_name': self.func_name,
                'source_lines': self.source_lines,
                'start_line': self.start_line,
                'source_file': self.source_filename,
                'debug_frames': self.debug_frames,
                'args': args,
                'kwargs': kwargs,
                'return_value': None,
                'exception': ('KeyboardInterrupt', 'Execution interrupted by user')
            }
        except Exception as e:
            return None, {
                'function_name': self.func_name,
                'source_lines': self.source_lines,
                'start_line': self.start_line,
                'source_file': self.source_filename,
                'debug_frames': self.debug_frames,
                'args': args,
                'kwargs': kwargs,
                'return_value': None,
                'exception': (type(e).__name__, str(e))
            }





class DebugExecutor:
    """
    Executor component responsible for running the target function
    and collecting execution information.
    """
    
    def __init__(self):
        """Initialize the executor."""
        self.debugger = LineDebugger()
    
    def execute(self, func, *args, **kwargs):
        """
        Execute the target function using the debugger and collect information.
        
        Args:
            func: The function to debug
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
            
        Returns:
            Tuple of (result, debug_info)
        """
        # Extract source_code from kwargs if provided
        source_code = kwargs.pop('source_code', None)
        start_line = kwargs.pop('start_line', 1)  # Default to line 1
     
        # Run the function with the debugger to get execution info
        result, debug_info = self.debugger.run_function(func, source_code, start_line, *args, **kwargs)
        return result, debug_info


def debug_function(func, *args, delay=1.0, auto_run=False, **kwargs):
    """
    Convenience function to debug and visualize a function execution.
    
    Args:
        func: The function to debug
        *args: Arguments to pass to the function
        delay: The delay between steps when auto-running (default: 1.0 seconds)
        auto_run: Whether to automatically run with delay or step through with Enter key (default: False)
        **kwargs: Keyword arguments to pass to the function
    """
    # Create a controller and use it to debug the function
    controller = DebugController(delay=delay, auto_run=auto_run)
    return controller.debug(func, *args, **kwargs)