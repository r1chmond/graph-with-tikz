from collections import OrderedDict
from typing import Any, List


def remove_duplicates(elements: List[Any]) -> None:
    """
    Remove duplicate elements from a list(hashable elements).
    Args:
        elements (List[Any]) -- List of elements to remove duplicates from.
    """
    # Check if the is not empty and elements are tuples
    if elements and isinstance(elements[0], tuple):
        seen = OrderedDict()
        for element in elements:
            if element[0] not in seen:
                seen[element[0]] = element
        elements.clear()
        elements.extend(list(seen.values()))

    else:
        seen = OrderedDict()
        for element in elements:
            if element not in seen:
                seen[element] = None
        elements.clear()
        elements.extend(list(seen.keys()))
