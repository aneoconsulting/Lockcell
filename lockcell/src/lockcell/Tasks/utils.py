# List manipulers


def split(tab: list, n: int):
    """Stub to overload in subclasses"""
    subsets = []
    start = 0
    for i in range(n):
        subset = tab[start : start + (len(tab) - start) // (n - i)]
        subsets.append(subset)
        start = start + len(subset)
    return subsets


def listminus(c1: list, c2: list):
    """Return a list of all elements of C1 that are not in C2."""
    s2 = {}
    for delta in c2:
        s2[delta] = 1

    c = []
    for delta in c1:
        if delta not in s2:
            c.append(delta)

    return c
