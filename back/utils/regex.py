
"""
Contains utility functions to works with request query parameters.
"""

import re


def only_letters(param):
    """Check if one param contains only letters."""
    return bool(re.compile(r'^[A-Z]+$', re.IGNORECASE).match(param))
