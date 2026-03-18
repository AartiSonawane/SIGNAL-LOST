---
day: 4
solver: vedh-sonawane
date: 2025-03-18
solution: "case_insensitive_string_replacement"
puzzle_type: code
---

# Day 4 Solution - String Replacement Challenge

## My Approach
Use regular expressions with case-insensitive flag to replace 'signal' with 'relay' and 'network' with 'array' while preserving the original case.

## Solution
```python
import re

def replace_terms(input_string):
    # Replace 'signal' with 'relay' (case-insensitive)
    result = re.sub(r'signal', 'relay', input_string, flags=re.IGNORECASE)
    
    # Replace 'network' with 'array' (case-insensitive)
    result = re.sub(r'network', 'array', result, flags=re.IGNORECASE)
    
    return result

# Test cases
print(replace_terms("The SIGNAL is strong"))  # "The relay is strong"
print(replace_terms("Network status: OK"))    # "array status: OK"
print(replace_terms("Signal and network"))    # "relay and array"
```

## Explanation
The function uses Python's `re.sub()` with the `re.IGNORECASE` flag to perform case-insensitive replacements:
1. First pass replaces all occurrences of 'signal' (any case) with 'relay'
2. Second pass replaces all occurrences of 'network' (any case) with 'array'
3. All other parts of the string remain unchanged

---
**Solver:** @vedh-sonawane
**Submitted:** 2025-03-18
**Status:** ⏳ Awaiting validation...
