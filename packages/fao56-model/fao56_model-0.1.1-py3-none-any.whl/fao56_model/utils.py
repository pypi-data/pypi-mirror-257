from typing import List

from datetimerange import DateTimeRange


def is_overlapping(list_range: List[DateTimeRange]) -> bool:
    """
    Returns True if list of DateTimeRange objects has any overlapping ranges
    """
    for i in range(len(list_range)):
        for j in range(i + 1, len(list_range)):
            if list_range[i].is_intersection(list_range[j]):
                return True
    return False
