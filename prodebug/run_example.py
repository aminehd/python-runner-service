from line_debugger import debug_function

# Example function to debug
def two_sum(nums, target):
    """Find indices of two numbers that add up to target"""
    # Sort the array for two-pointer approach
    sorted_nums = sorted(nums)
    
    # Initial pointers
    left = 0
    right = len(sorted_nums) - 1
    
    # Main algorithm
    while left < right:
        current_sum = sorted_nums[left] + sorted_nums[right]
        
        if current_sum == target:
            # Return the positions
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return []

# Another two-pointer example: binary search
def binary_search(arr, target):
    """Find target in sorted array using binary search"""
    low = 0
    high = len(arr) - 1
    
    while low <= high:
        mid = (low + high) // 2
        current = arr[mid]
        
        if current == target:
            return mid
        elif current < target:
            low = mid + 1
        else:
            high = mid - 1
    
    return -1

# Another two-pointer example: palindrome check
def is_palindrome(s):
    """Check if string is a palindrome using two pointers"""
    # Preprocess the string: convert to lowercase and remove non-alphanumeric
    s = ''.join(c.lower() for c in s if c.isalnum())
    
    # Use two pointers from both ends
    left = 0
    right = len(s) - 1
    
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    
    return True

# Sorting algorithm example: bubble sort
def bubble_sort(arr):
    """Sort an array using bubble sort algorithm"""
    n = len(arr)
    swaps = 0
    comparisons = 0
    
    # Create a copy to avoid modifying the original
    array = arr.copy()
    
    for i in range(n):
        # Flag to optimize if no swaps occur in a pass
        swapped = False
        
        for j in range(0, n - i - 1):
            comparisons += 1
            
            # Compare adjacent elements
            if array[j] > array[j + 1]:
                # Swap them
                array[j], array[j + 1] = array[j + 1], array[j]
                swaps += 1
                swapped = True
        
        # If no swapping occurred in this pass, array is sorted
        if not swapped:
            break
    
    return array, swaps, comparisons

# Sorting algorithm example: quick sort with instrumentation
def quick_sort(arr):
    """Sort an array using quick sort algorithm with instrumentation"""
    # Create a copy to avoid modifying the original
    array = arr.copy()
    
    # Initialize counters
    swaps = 0
    comparisons = 0
    
    # Inner function to do the recursive sorting
    def _quick_sort(arr, low, high):
        nonlocal swaps, comparisons
        
        if low < high:
            # Partition the array and get the pivot index
            pivot_idx, s, c = partition(arr, low, high)
            swaps += s
            comparisons += c
            
            # Recursively sort the sub-arrays
            _quick_sort(arr, low, pivot_idx - 1)
            _quick_sort(arr, pivot_idx + 1, high)
    
    # Partition function
    def partition(arr, low, high):
        local_swaps = 0
        local_comparisons = 0
        
        # Choose the rightmost element as pivot
        pivot = arr[high]
        
        # Index of smaller element
        i = low - 1
        
        for j in range(low, high):
            local_comparisons += 1
            # If current element is smaller than or equal to pivot
            if arr[j] <= pivot:
                # Increment index of smaller element
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                local_swaps += 1
        
        # Place pivot in its correct position
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        local_swaps += 1
        
        return i + 1, local_swaps, local_comparisons
    
    # Start the sorting
    _quick_sort(array, 0, len(array) - 1)
    
    return array, swaps, comparisons

if __name__ == "__main__":
    # Set the delay between steps
    delay = 2  # 0.5 second delay between lines
    
    # Run the two_sum function
    print("\n=== Running two_sum ===")
    result = debug_function(two_sum, [1, 4, 6, 8, 9, 11, 15, 17], 15, delay=delay, auto_run=True)
    print(f"Final result: {result}")
    
    # Run the binary_search function
    # print("\n=== Running binary_search ===")
    # result = debug_function(binary_search, [1, 3, 5, 7, 9, 11, 13, 15], 7, delay=delay, auto_run=True)
    # print(f"Final result: {result}")
    
    # # Run the is_palindrome function
    # print("\n=== Running is_palindrome ===")
    # result = debug_function(is_palindrome, "A man, a plan, a canal: Panama", delay=delay, auto_run=True)
    # print(f"Final result: {result}")
    
    # # Run the bubble_sort function
    # print("\n=== Running bubble_sort ===")
    # unsorted_array = [64, 34, 25, 12, 22, 11, 90]
    # result = debug_function(bubble_sort, unsorted_array, delay=delay, auto_run=True)
    # print(f"Final result: {result}")
    
    # # Run the quick_sort function
    # print("\n=== Running quick_sort ===")
    # unsorted_array = [38, 27, 43, 3, 9, 82, 10]
    # result = debug_function(quick_sort, unsorted_array, delay=delay, auto_run=True)
    # print(f"Final result: {result}")