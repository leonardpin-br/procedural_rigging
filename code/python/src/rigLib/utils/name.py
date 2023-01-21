# -*- coding: utf-8 -*-
u"""name @ utils

Utilities to work with names and strings.
"""

def removeSuffix(name):
    """Remove suffix from given name string.

    Args:
        name (str): Given name string to process.

    Returns:
        str: Name without suffix.
    """

    edits = name.split("_")

    if len(edits) < 2:
        return name

    suffix = "_" + edits[-1]
    nameNoSuffix = name[:-len(suffix)]

    return nameNoSuffix