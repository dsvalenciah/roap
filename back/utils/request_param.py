
"""
Contains utility functions to works with request query parameters.
"""

import re

only_letters = re.compile(r'^[A-Z]+$', re.IGNORECASE)


def is_correct_parameter(param):
    """Check if one param contains only letters."""
    return bool(only_letters.match(param))
