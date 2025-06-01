"""
Visualization utilities for algorithm debugging.
This module contains classes and functions for visualizing algorithm execution.
"""

import os
import time
from colorama import Fore, Style, init

# Initialize colorama for when we need to print outside of asciimatics
init()

# Algorithm detection functions
def is_two_pointer_algorithm(func_name):
    """Check if a function name suggests it's a two-pointer algorithm."""
    two_pointer_keywords = ['two', 'pair', 'pointer', 'binary_search', 
                           'search', 'find', 'sum', 'palindrome', 'reverse']
    return any(keyword in func_name.lower() for keyword in two_pointer_keywords)

def is_sorting_algorithm(func_name):
    """Check if a function name suggests it's a sorting algorithm."""
    sorting_keywords = ['sort', 'bubble', 'insertion', 'selection', 'merge', 'quick', 'heap', 
                       'radix', 'counting', 'shell', 'partition']
    return any(keyword in func_name.lower() for keyword in sorting_keywords)

# State detection functions
def detect_array_and_pointers(variables):
    """Detect array and pointer variables in a two-pointer algorithm."""
    result = {
        'array': None,
        'left_pointer': None,
        'right_pointer': None,
        'target': None,
        'current': None
    }
    
    # Try to identify the array variable (common names)
    for var_name in ['arr', 'nums', 'array', 'sorted_nums', 'data', 's']:
        if var_name in variables:
            try:
                value = eval(variables[var_name])
                # Make sure it's an array-like object
                if hasattr(value, '__len__') and hasattr(value, '__getitem__'):
                    result['array'] = (var_name, value)
                    break
            except:
                pass
                
    # Try to identify pointer variables
    for left_name in ['left', 'i', 'start', 'low', 'l', 'p1']:
        if left_name in variables:
            try:
                result['left_pointer'] = (left_name, int(variables[left_name]))
                break
            except:
                pass
                
    for right_name in ['right', 'j', 'end', 'high', 'r', 'p2']:
        if right_name in variables:
            try:
                result['right_pointer'] = (right_name, int(variables[right_name]))
                break
            except:
                pass
    
    # Try to identify target or comparison variables
    for target_name in ['target', 'goal', 'sum_target', 'k']:
        if target_name in variables:
            try:
                result['target'] = (target_name, eval(variables[target_name]))
                break
            except:
                pass
                
    for comp_name in ['current_sum', 'sum', 'total', 'current', 'current', 'mid']:
        if comp_name in variables:
            try:
                result['current'] = (comp_name, eval(variables[comp_name]))
                break
            except:
                pass
                
    return result


def detect_sorting_algorithm_state(variables, current_line=None, source_lines=None, current_line_idx=None):
    """Detect array and indices for a sorting algorithm."""
    result = {
        'array': None,
        'primary_index': None,
        'secondary_index': None,
        'pivot': None,
        'swaps': None,
        'comparisons': None,
        'phase': None,
        'highlighted_indices': [],
        'swapping_indices': []
    }
    
    # Try to identify the array variable
    for var_name in ['arr', 'nums', 'array', 'list', 'data', 'a']:
        if var_name in variables:
            try:
                value = eval(variables[var_name])
                # Make sure it's an array-like object
                if hasattr(value, '__len__') and hasattr(value, '__getitem__'):
                    result['array'] = (var_name, value)
                    break
            except:
                pass
                
    # Try to identify index variables
    for primary_name in ['i', 'index', 'current', 'pos', 'idx']:
        if primary_name in variables:
            try:
                result['primary_index'] = (primary_name, int(variables[primary_name]))
                # Add to highlighted indices
                result['highlighted_indices'].append(int(variables[primary_name]))
                break
            except:
                pass
                
    for secondary_name in ['j', 'next_index', 'right', 'end']:
        if secondary_name in variables:
            try:
                result['secondary_index'] = (secondary_name, int(variables[secondary_name]))
                # Add to highlighted indices
                result['highlighted_indices'].append(int(variables[secondary_name]))
                break
            except:
                pass
                
    # Try to identify pivot for quick sort
    for pivot_name in ['pivot', 'pivot_value', 'p', 'piv']:
        if pivot_name in variables:
            try:
                result['pivot'] = (pivot_name, eval(variables[pivot_name]))
                break
            except:
                pass
                
    # Try to identify swap and comparison counters
    for swap_name in ['swaps', 'swap_count', 'num_swaps']:
        if swap_name in variables:
            try:
                result['swaps'] = (swap_name, int(variables[swap_name]))
                break
            except:
                pass
                
    for comp_name in ['comparisons', 'comparison_count', 'comps']:
        if comp_name in variables:
            try:
                result['comparisons'] = (comp_name, int(variables[comp_name]))
                break
            except:
                pass
    
    # Try to determine phase based on current line
    if current_line and source_lines and current_line_idx is not None:
        current_src_line = source_lines[current_line_idx].lower().strip()
        
        # Check for common sorting operations
        if "swap" in current_src_line:
            result['phase'] = "SWAPPING"
            # If we have both indices, they're probably being swapped
            if result['primary_index'] and result['secondary_index']:
                result['swapping_indices'] = [
                    result['primary_index'][1],
                    result['secondary_index'][1]
                ]
        elif "<" in current_src_line or ">" in current_src_line or "compare" in current_src_line:
            result['phase'] = "COMPARING"
        elif "pivot" in current_src_line:
            result['phase'] = "SELECTING_PIVOT"
        elif "partition" in current_src_line:
            result['phase'] = "PARTITIONING"
        else:
            result['phase'] = "ITERATING"
    
    return result

# Visualization functions
def create_progress_bar(progress, width=50):
    """Create a visually appealing progress bar with percentage."""
    filled_width = int(width * progress / 100)
    bar = '█' * filled_width + '░' * (width - filled_width)
    return f"[{bar}] {progress:.1f}%"

def display_code_with_effects(source_lines, current_line, start_line):
    """Display code with enhanced visual effects."""
    # Determine suitable window size (show context around current line)
    context_lines = 5
    current_idx = current_line - start_line
    
    # Calculate display window
    total_lines = len(source_lines)
    
    # Create box borders for code display
    width = max(max(len(line) for line in source_lines) + 12, 60)
    box_top = f"╔══ {Fore.CYAN}CODE{Style.RESET_ALL} " + "═" * (width - 9) + "╗"
    box_bottom = "╚" + "═" * (width - 2) + "╝"
    
    # Start with box top
    output = [box_top]
    
    # Add all lines with appropriate highlighting
    for j, line in enumerate(source_lines):
        line_num = j + start_line
        
        # Format line number with padding for alignment 
        line_num_str = f"{line_num:4d}"
        
        # Format the line differently based on whether it's the current line
        if line_num == current_line:
            # Highlight the current line with bright green and an arrow
            formatted_line = f"║ {Fore.WHITE}{Style.BRIGHT}{line_num_str}{Style.RESET_ALL} │ {Fore.GREEN}{Style.BRIGHT}→ {line.rstrip()}{Style.RESET_ALL}"
        else:
            # Make other lines dimmer
            formatted_line = f"║ {Fore.BLUE}{line_num_str}{Style.RESET_ALL} │ {Fore.LIGHTBLACK_EX}{line.rstrip()}{Style.RESET_ALL}"
        
        # Pad the line to align with the box
        padding = width - len(formatted_line.replace(Fore.WHITE, "")
                                      .replace(Style.BRIGHT, "")
                                      .replace(Style.RESET_ALL, "")
                                      .replace(Fore.GREEN, "")
                                      .replace(Fore.BLUE, "")
                                      .replace(Fore.LIGHTBLACK_EX, "")) - 1
        formatted_line += " " * padding + "║"
        
        output.append(formatted_line)
    
    # Add box bottom
    output.append(box_bottom)
    
    return "\n".join(output)

def display_variables_table(variables):
    """Display variables in a pretty table format."""
    if not variables:
        return "No variables to display"
    
    # Find the longest variable name for formatting
    longest_name = max(len(name) for name in variables.keys() if not name.startswith('_'))
    longest_value = min(max(len(str(value)) for name, value in variables.items() 
                          if not name.startswith('_')), 50)  # Limit to 50 chars
    
    # Create a nice table header
    width = longest_name + longest_value + 7
    header = f"╔══ {Fore.YELLOW}VARIABLES{Style.RESET_ALL} " + "═" * (width - 14) + "╗"
    separator = f"╟{'─' * (longest_name + 2)}┼{'─' * (longest_value + 2)}╢"
    footer = "╚" + "═" * (width - 2) + "╝"
    
    # Start with header
    table = [header]
    
    # Add column headers
    table.append(f"║ {Fore.CYAN}{Style.BRIGHT}{'Name':<{longest_name}}{Style.RESET_ALL} │ {Fore.CYAN}{Style.BRIGHT}{'Value':<{longest_value}}{Style.RESET_ALL} ║")
    table.append(separator)
    
    # Add each variable
    for name, value in sorted(variables.items()):
        if not name.startswith('_'):
            # Truncate very long values
            value_str = str(value)
            if len(value_str) > longest_value:
                value_str = value_str[:longest_value-3] + "..."
                
            # Format the line
            table.append(f"║ {Fore.GREEN}{name:<{longest_name}}{Style.RESET_ALL} │ {value_str:<{longest_value}} ║")
    
    # Add footer
    table.append(footer)
    
    return "\n".join(table)

def create_fancy_header(title, width=80):
    """Create a fancy title header with box drawing chars."""
    padding = (width - len(title) - 4) // 2
    return f"╔{'═' * padding} {Fore.CYAN}{Style.BRIGHT}{title}{Style.RESET_ALL} {'═' * padding}╗"

def visualize_array_with_pointers(array_data, left_ptr=None, right_ptr=None):
    """Visualize an array with pointers using elaborate ASCII art."""
    if not array_data:
        return
        
    array_name, array = array_data
    
    # Create fancy border and header
    width = max(len(array) * 4 + 10, 40)  # Width based on array size
    border_top = f"╔{'═' * (width-2)}╗"
    border_bottom = f"╚{'═' * (width-2)}╝"
    
    # Create header with fancy styling
    header = f"╔{'═' * 10}╡ {Fore.CYAN}{Style.BRIGHT}Array: {array_name} [{len(array)} elements]{Style.RESET_ALL} ╞{'═' * 10}╗"
    
    # Start building the output
    output = [header]
    
    # Add a row separator
    output.append(f"╟{'─' * (width - 2)}╢")
    
    # Create index line with box drawing chars
    index_line = f"║ {Fore.BLUE}Index:{Style.RESET_ALL} "
    for i in range(len(array)):
        index_line += f"{Fore.BLUE}{i:^4}{Style.RESET_ALL}"
    # Pad the end to align with the border
    padding = width - len(index_line.replace(Fore.BLUE, "").replace(Style.RESET_ALL, "")) - 1
    index_line += " " * padding + "║"
    output.append(index_line)
    
    # Create value line with box drawing chars and better highlighting
    value_line = f"║ {Fore.GREEN}Value:{Style.RESET_ALL} "
    for i, val in enumerate(array):
        # Highlight values at pointer positions
        if (left_ptr and i == left_ptr[1]) or (right_ptr and i == right_ptr[1]):
            value_line += f"{Fore.MAGENTA}{Style.BRIGHT}{val:^4}{Style.RESET_ALL}"
        else:
            value_line += f"{val:^4}"
    # Pad the end to align with the border
    padding = width - len(value_line.replace(Fore.GREEN, "").replace(Style.RESET_ALL, "").replace(Fore.MAGENTA, "").replace(Style.BRIGHT, "")) - 1
    value_line += " " * padding + "║"
    output.append(value_line)
    
    # Create nice looking separator with pointer positions highlighted
    sep_line = "║ " + "─" * (width - 4) + " ║"
    output.append(sep_line)
    
    # Create pointer line with better indicators that align with the numbers
    pointer_line = "║      "
    for i in range(len(array)):
        if left_ptr and i == left_ptr[1] and right_ptr and i == right_ptr[1]:
            pointer_line += f"{Fore.MAGENTA}{'⬍':^4}{Style.RESET_ALL}"  # Both pointers
        elif left_ptr and i == left_ptr[1]:
            pointer_line += f"{Fore.YELLOW}{'⬆':^4}{Style.RESET_ALL}"  # Left pointer
        elif right_ptr and i == right_ptr[1]:
            pointer_line += f"{Fore.CYAN}{'⬇':^4}{Style.RESET_ALL}"    # Right pointer
        else:
            pointer_line += f"{' ':^4}"
    # Pad the end to align with the border
    padding = width - len(pointer_line.replace(Fore.YELLOW, "").replace(Style.RESET_ALL, "").replace(Fore.CYAN, "").replace(Fore.MAGENTA, "")) - 1
    pointer_line += " " * padding + "║"
    output.append(pointer_line)
    
    # Add pointer labels in a more appealing way
    if left_ptr or right_ptr:
        label_line = "║      "
        for i in range(len(array)):
            if left_ptr and i == left_ptr[1]:
                label_line += f"{Fore.YELLOW}{left_ptr[0]:^4}{Style.RESET_ALL}"
            elif right_ptr and i == right_ptr[1]:
                label_line += f"{Fore.CYAN}{right_ptr[0]:^4}{Style.RESET_ALL}"
            else:
                label_line += f"{' ':^4}"
        # Pad the end to align with the border
        padding = width - len(label_line.replace(Fore.YELLOW, "").replace(Style.RESET_ALL, "").replace(Fore.CYAN, "")) - 1
        label_line += " " * padding + "║"
        output.append(label_line)
    
    # Add bottom border
    output.append(border_bottom)
    
    return "\n".join(output)

def visualize_sorting_array(array_data, highlighted_indices=None, swapping_indices=None, phase=None):
    """Visualize a sorting array with highlighted indices using Unicode box drawing characters."""
    if not array_data:
        return
        
    array_name, array = array_data
    highlighted_indices = highlighted_indices or []
    swapping_indices = swapping_indices or []
    
    # Create fancy border and header
    width = max(len(array) * 4 + 10, 60)  # Width based on array size
    
    # Create header with fancy styling
    header = f"╔{'═' * 10}╡ {Fore.CYAN}{Style.BRIGHT}Sorting Array: {array_name} [{len(array)} elements]{Style.RESET_ALL} ╞{'═' * 10}╗"
    
    # Start building the output
    output = [header]
    
    # Add a row separator
    output.append(f"╟{'─' * (width - 2)}╢")
    
    # Create index line
    index_line = f"║ {Fore.BLUE}Index:{Style.RESET_ALL} "
    for i in range(len(array)):
        index_line += f"{Fore.BLUE}{i:^4}{Style.RESET_ALL}"
    # Pad the end to align with the border
    padding = width - len(index_line.replace(Fore.BLUE, "").replace(Style.RESET_ALL, "")) - 1
    index_line += " " * padding + "║"
    output.append(index_line)
    
    # Create value line with special formatting for sorting operations
    value_line = f"║ {Fore.GREEN}Value:{Style.RESET_ALL} "
    for i, val in enumerate(array):
        # Different highlighting for different states
        if i in swapping_indices:
            value_line += f"{Fore.MAGENTA}{Style.BRIGHT}[{val:^2}]{Style.RESET_ALL}" # Swapping
        elif i in highlighted_indices:
            value_line += f"{Fore.YELLOW}{Style.BRIGHT}*{val:^2}*{Style.RESET_ALL}" # Current pointers
        else:
            value_line += f"{val:^4}"
    # Pad the end
    padding = width - len(value_line.replace(Fore.GREEN, "")
                                .replace(Style.RESET_ALL, "")
                                .replace(Fore.YELLOW, "")
                                .replace(Style.BRIGHT, "")
                                .replace(Fore.MAGENTA, "")) - 1
    value_line += " " * padding + "║"
    output.append(value_line)
    
    # Create operation indicators
    marker_line = f"║ {Fore.CYAN}Op:{Style.RESET_ALL}    "
    for i in range(len(array)):
        if i in swapping_indices:
            marker_line += f"{Fore.MAGENTA}↕   {Style.RESET_ALL}" # Swap
        elif i in highlighted_indices and phase == "COMPARING":
            marker_line += f"{Fore.YELLOW}?   {Style.RESET_ALL}" # Compare
        elif i in highlighted_indices and phase == "SELECTING_PIVOT":
            marker_line += f"{Fore.CYAN}P   {Style.RESET_ALL}" # Pivot
        else:
            marker_line += "    "
    # Pad the end
    padding = width - len(marker_line.replace(Fore.CYAN, "")
                                 .replace(Style.RESET_ALL, "")
                                 .replace(Fore.YELLOW, "")
                                 .replace(Fore.MAGENTA, "")) - 1
    marker_line += " " * padding + "║"
    output.append(marker_line)
    
    # Add phase information if available
    if phase:
        output.append(f"║ {Fore.CYAN}Phase:{Style.RESET_ALL} {phase}{' ' * (width - 9 - len(phase))}║")
    
    # Add bottom border
    output.append(f"╚{'═' * (width - 2)}╝")
    
    return "\n".join(output)

def simple_visualize(debug_info, delay=1.0, auto_run=False):
    """
    A visually enhanced visualization using terminal output with effects.
    
    Args:
        debug_info: Debug information from LineDebugger
        delay: Delay between steps when auto-running (default: 1.0 seconds)
        auto_run: Whether to automatically run with delay or step through with Enter key (default: False)
    """
    import os
    import time
    import select
    import sys
    from colorama import Fore, Style

    function_name = debug_info['function_name']
    args = debug_info['args']
    debug_frames = debug_info['debug_frames']
    
    # Detect algorithm type
    is_two_pointer = is_two_pointer_algorithm(function_name)
    is_sorting = is_sorting_algorithm(function_name)
    
    # Create a fancy header
    width = os.get_terminal_size().columns if hasattr(os, 'get_terminal_size') else 80
    header = create_fancy_header(f"Debugging {function_name}", width)
    
    run_mode = "AUTO" if auto_run else "INTERACTIVE"
    
    # Show startup screen with animation
    os.system('cls' if os.name == 'nt' else 'clear')
    print(header)
    print(f"╟{'─' * (width - 2)}╢")
    print(f"║ {Fore.CYAN}Function:{Style.RESET_ALL} {function_name}")
    print(f"║ {Fore.CYAN}Arguments:{Style.RESET_ALL} {', '.join([repr(arg) for arg in args])}")
    print(f"║ {Fore.CYAN}Total Steps:{Style.RESET_ALL} {len(debug_frames)}")
    print(f"║ {Fore.CYAN}Mode:{Style.RESET_ALL} {Fore.GREEN if auto_run else Fore.YELLOW}{run_mode}{Style.RESET_ALL} " + 
          f"({'delay: ' + str(delay) + 's' if auto_run else 'press Enter to advance'})")
    
    # Show detected algorithm type
    if is_two_pointer:
        print(f"║ {Fore.CYAN}Algorithm:{Style.RESET_ALL} Two-pointer algorithm detected")
    elif is_sorting:
        print(f"║ {Fore.CYAN}Algorithm:{Style.RESET_ALL} Sorting algorithm detected")
    
    print(f"║ {Fore.CYAN}Controls:{Style.RESET_ALL} " + 
          (f"Press {Fore.YELLOW}Ctrl+C{Style.RESET_ALL} to exit, {Fore.YELLOW}Space{Style.RESET_ALL} to toggle mode" if auto_run else
           f"Press {Fore.YELLOW}Enter{Style.RESET_ALL} to step, {Fore.YELLOW}Space{Style.RESET_ALL} to toggle auto-run, {Fore.YELLOW}Ctrl+C{Style.RESET_ALL} to exit"))
    print(f"╚{'═' * (width - 2)}╝")
    
    # Countdown effect
    print("\nStarting in:")
    for i in range(3, 0, -1):
        print(f"{Fore.YELLOW}{Style.BRIGHT}{i}...{Style.RESET_ALL}", end="", flush=True)
        time.sleep(0.5)
    print(f"{Fore.GREEN}{Style.BRIGHT}Go!{Style.RESET_ALL}")
    time.sleep(0.5)
    
    # Start in the requested mode
    current_mode = auto_run
    
    try:
        # Visualize each step
        step_idx = 0
        while step_idx < len(debug_frames):
            frame = debug_frames[step_idx]
            
            # Clear screen
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Display a visually appealing header with progress
            total_steps = len(debug_frames)
            progress = (step_idx + 1) / total_steps * 100
            
            # Current mode indicator for display
            mode_str = f"{Fore.GREEN}AUTO{Style.RESET_ALL}" if current_mode else f"{Fore.YELLOW}INTERACTIVE{Style.RESET_ALL}"
            
            # Box-drawing header with progress info
            print(header)
            print(f"╟{'─' * (width - 2)}╢")
            print(f"║ {Fore.CYAN}Step:{Style.RESET_ALL} {step_idx+1}/{total_steps}  {Fore.CYAN}Line:{Style.RESET_ALL} {frame.current_line}  {Fore.CYAN}Progress:{Style.RESET_ALL} {progress:.1f}%")
            progress_bar = create_progress_bar(progress, width - 20)
            print(f"║ {progress_bar}")
            print(f"║ {Fore.CYAN}Mode:{Style.RESET_ALL} {mode_str}")
            print(f"╟{'─' * (width - 2)}╢")
            print()
            
            # Show code with enhanced display
            code_display = display_code_with_effects(frame.source_lines, frame.current_line, frame.start_line)
            print(code_display)
            print()
            
            # Enhanced visualization for two-pointer algorithms
            if is_two_pointer:
                # Try to detect array and pointers
                algo_state = detect_array_and_pointers(frame.variables)
                
                # If we found both array and at least one pointer, show enhanced visualization
                if algo_state['array'] and (algo_state['left_pointer'] or algo_state['right_pointer']):
                    array_vis = visualize_array_with_pointers(
                        algo_state['array'],
                        algo_state['left_pointer'],
                        algo_state['right_pointer']
                    )
                    if array_vis:
                        print(array_vis)
                    
                    # Show target and current value if available with fancy box
                    if algo_state['target'] and algo_state['current']:
                        target_name, target_val = algo_state['target']
                        current_name, current_val = algo_state['current']
                        
                        # Create a nice box for algorithm state
                        print(f"╔══ {Fore.YELLOW}Algorithm State{Style.RESET_ALL} ═════════════╗")
                        print(f"║ {Fore.CYAN}{target_name}:{Style.RESET_ALL} {target_val:<16} ║")
                        
                        # Format current value based on comparison with target
                        if current_val == target_val:
                            print(f"║ {Fore.CYAN}{current_name}:{Style.RESET_ALL} {Fore.GREEN}{Style.BRIGHT}{current_val}{Style.RESET_ALL} {Fore.GREEN}(Match found!){Style.RESET_ALL} ║")
                        elif current_val < target_val:
                            print(f"║ {Fore.CYAN}{current_name}:{Style.RESET_ALL} {Fore.YELLOW}{current_val}{Style.RESET_ALL} {Fore.YELLOW}(Too small){Style.RESET_ALL} ║")
                        else:
                            print(f"║ {Fore.CYAN}{current_name}:{Style.RESET_ALL} {Fore.YELLOW}{current_val}{Style.RESET_ALL} {Fore.YELLOW}(Too large){Style.RESET_ALL} ║")
                        print(f"╚════════════════════════════════╝")
            
            # Enhanced visualization for sorting algorithms
            elif is_sorting:
                # Current line index for line-based analysis
                current_line_idx = frame.current_line - frame.start_line
                
                # Try to detect sorting algorithm state
                algo_state = detect_sorting_algorithm_state(
                    frame.variables, 
                    frame.current_line, 
                    frame.source_lines, 
                    current_line_idx
                )
                
                # If we found an array and indices, show enhanced visualization
                if algo_state['array']:
                    array_vis = visualize_sorting_array(
                        algo_state['array'],
                        algo_state['highlighted_indices'],
                        algo_state['swapping_indices'],
                        algo_state['phase']
                    )
                    if array_vis:
                        print(array_vis)
                    
                    # Show sorting statistics if available
                    if algo_state['swaps'] or algo_state['comparisons']:
                        # Create a nice box for algorithm metrics
                        print(f"╔══ {Fore.YELLOW}Sorting Metrics{Style.RESET_ALL} ════════════╗")
                        
                        if algo_state['swaps']:
                            swap_name, swap_val = algo_state['swaps']
                            print(f"║ {Fore.CYAN}{swap_name}:{Style.RESET_ALL} {swap_val:<16} ║")
                            
                        if algo_state['comparisons']:
                            comp_name, comp_val = algo_state['comparisons']
                            print(f"║ {Fore.CYAN}{comp_name}:{Style.RESET_ALL} {comp_val:<16} ║")
                            
                        print(f"╚═══════════════════════════════╝")
                    
                    # Show primary and secondary index information
                    if algo_state['primary_index'] or algo_state['secondary_index']:
                        # Create index info box
                        print(f"╔══ {Fore.YELLOW}Current Indices{Style.RESET_ALL} ════════════╗")
                        
                        if algo_state['primary_index']:
                            idx_name, idx_val = algo_state['primary_index'] 
                            print(f"║ {Fore.CYAN}{idx_name}:{Style.RESET_ALL} {idx_val:<16} ║")
                            
                        if algo_state['secondary_index']:
                            idx_name, idx_val = algo_state['secondary_index']
                            print(f"║ {Fore.CYAN}{idx_name}:{Style.RESET_ALL} {idx_val:<16} ║")
                            
                        print(f"╚═══════════════════════════════╝")
            
            # Show variables in a nicely formatted table
            filtered_vars = {k: v for k, v in frame.variables.items() if not k.startswith('_')}
            if filtered_vars:
                print("\n" + display_variables_table(filtered_vars))
            
            # Show controls based on mode
            if step_idx < len(debug_frames) - 1:
                if current_mode:  # Auto mode
                    # Show controls with auto-run info
                    print(f"\n{Fore.CYAN}[Space]{Style.RESET_ALL} Toggle to interactive | {Fore.CYAN}[Ctrl+C]{Style.RESET_ALL} Exit")
                    
                    # Wait for the specified delay, but also check for keypress to toggle mode
                    start_time = time.time()
                    while time.time() - start_time < delay:
                        # Check if there's input available (non-blocking)
                        rlist, _, _ = select.select([sys.stdin], [], [], 0)
                        if rlist:
                            # Read the key input
                            key = sys.stdin.read(1)
                            if key == ' ':  # Space key toggles mode
                                current_mode = not current_mode
                                print(f"\nSwitched to {Fore.YELLOW}INTERACTIVE{Style.RESET_ALL} mode")
                                time.sleep(0.5)  # Brief pause to show the message
                                break  # Exit the delay loop
                        
                        # Brief sleep to reduce CPU usage
                        time.sleep(0.1)
                        
                    # If we're still in auto mode, advance to next step
                    if current_mode:
                        step_idx += 1
                    
                else:  # Interactive mode
                    # Show controls for interactive mode
                    print(f"\n{Fore.CYAN}[Enter]{Style.RESET_ALL} Next step | {Fore.CYAN}[Space]{Style.RESET_ALL} Toggle to auto-run | {Fore.CYAN}[Ctrl+C]{Style.RESET_ALL} Exit")
                    try:
                        # Wait for Enter or Space
                        key = input("")
                        if key == " ":  # Space toggles to auto mode
                            current_mode = True
                            print(f"\nSwitched to {Fore.GREEN}AUTO{Style.RESET_ALL} mode")
                            time.sleep(0.5)  # Brief pause
                        step_idx += 1  # Advance to next step
                    except KeyboardInterrupt:
                        print(f"\n{Fore.YELLOW}Execution interrupted by user{Style.RESET_ALL}")
                        break
            else:
                # We're on the last frame, just wait for any key
                input("\nPress Enter to see the final result...")
                step_idx += 1
            
        # Show final result with a fancy completion box
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Create a completion header
        completion_width = 60
        print(f"╔{'═' * (completion_width - 2)}╗")
        print(f"║{' ' * ((completion_width - 20) // 2)}{Fore.GREEN}{Style.BRIGHT}Execution Complete{Style.RESET_ALL}{' ' * ((completion_width - 20) // 2)}║")
        print(f"╟{'─' * (completion_width - 2)}╢")
        
        # Show result or exception
        if debug_info['return_value'] is not None:
            result_str = str(debug_info['return_value'])
            print(f"║ {Fore.CYAN}Function:{Style.RESET_ALL} {function_name}{' ' * (completion_width - 11 - len(function_name))}║")
            print(f"║ {Fore.CYAN}Result:{Style.RESET_ALL}   {Fore.GREEN}{result_str}{Style.RESET_ALL}{' ' * (completion_width - 10 - len(result_str))}║")
            print(f"╚{'═' * (completion_width - 2)}╝")
        elif debug_info['exception']:
            exc_type, exc_msg = debug_info['exception']
            print(f"║ {Fore.CYAN}Function:{Style.RESET_ALL} {function_name}{' ' * (completion_width - 11 - len(function_name))}║")
            print(f"║ {Fore.RED}Exception: {exc_type}: {exc_msg}{Style.RESET_ALL}{' ' * (completion_width - 13 - len(exc_type) - len(exc_msg))}║")
            print(f"╚{'═' * (completion_width - 2)}╝")
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Visualization stopped{Style.RESET_ALL}")


class TerminalVisualizer:
    """
    Terminal-based visualization component for displaying the debugging process.
    """
    
    def __init__(self, algorithm_type="generic"):
        """
        Initialize the visualizer.
        
        Args:
            algorithm_type: Type of algorithm to visualize (generic, two-pointer, sorting)
        """
        self.algorithm_type = algorithm_type
    
    def visualize(self, debug_info, delay=1.0, auto_run=False):
        """
        Visualize the debug information in the terminal.
        
        Args:
            debug_info: Debug information to visualize
            delay: Delay between steps in auto-run mode
            auto_run: Whether to start in auto-run mode
        """
        # Use the terminal visualization
        simple_visualize(debug_info, delay=delay, auto_run=auto_run)


class DebugController:
    """
    Controller class that orchestrates the debugging process.
    Follows the MVC pattern where:
    - Controller: This class, manages the execution flow
    - Model: LineDebugger and DebugFrame to capture execution state
    - View: Visualizers to display the execution
    """
    
    def __init__(self, delay=1.0, auto_run=False):
        """
        Initialize the controller with configuration.
        
        Args:
            delay: Delay between steps in auto-run mode
            auto_run: Whether to start in auto-run mode
        """
        self.delay = delay
        self.auto_run = auto_run
        self.executor = DebugExecutor()
        
    def debug(self, func, *args, **kwargs):
        """
        Main debugging entry point - coordinates execution and visualization.
        
        Args:
            func: The function to debug
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
        
        Returns:
            Result of the function execution
        """
        # Execute the function and collect debug info
        result, debug_info = self.executor.execute(func, *args, **kwargs)
        
        # Select appropriate visualizer based on algorithm detection
        visualizer = self._select_visualizer(debug_info)
        
        # Visualize the execution
        visualizer.visualize(debug_info, delay=self.delay, auto_run=self.auto_run)
        
        return result
    
    def _select_visualizer(self, debug_info):
        """
        Select the appropriate visualizer based on the algorithm type.
        
        Args:
            debug_info: Debug information collected during execution
            
        Returns:
            An appropriate visualizer instance
        """
        function_name = debug_info['function_name']
        
        # Detect algorithm type
        if is_two_pointer_algorithm(function_name):
            # For terminal-based visualization
            return TerminalVisualizer(algorithm_type="two-pointer")
        elif is_sorting_algorithm(function_name):
            # For terminal-based visualization
            return TerminalVisualizer(algorithm_type="sorting")
        else:
            # Generic visualizer as fallback
            return TerminalVisualizer(algorithm_type="generic")