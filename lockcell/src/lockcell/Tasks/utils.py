from enum import Enum

from pymonik import task


def split_list(tab: list, n: int):
    """
    Split a list into `n` nearly equal parts (difference of at most 1 element).

    Args:
        tab (list): The list to split.
        n (int): The number of parts to create.

    Returns:
        List[list]: A list of `n` disjoint sublists of `tab` (original order preserved).
    """
    subsets = []
    start = 0
    for i in range(n):
        subset = tab[start : start + (len(tab) - start) // (n - i)]
        subsets.append(subset)
        start = start + len(subset)
    return subsets


def AminusB(A: list, B: list):
    """
    Return the elements present in list `A` but not in list `B`.

    This performs a set-like difference while preserving the order of elements
    from `A`. Duplicate elements in `A` are kept as long as they are not in `B`.

    Args:
        A (list): The source list.
        B (list): The list of elements to exclude.

    Returns:
        list: A new list containing all items from `A` that are not in `B`.
    """
    s2 = {}
    for delta in B:
        s2[delta] = 1

    c = []
    for delta in A:
        if delta not in s2:
            c.append(delta)

    return c


class TaskTag(Enum):
    CLASSIC = "classic"
    THROWN = "thrown"
    ROOT = "root"
    END_ROOT = "end_root"
    RDDMIN_CHAIN = "rddmin_chain"


@task
def thrower(data: list[list]):
    return data, False
