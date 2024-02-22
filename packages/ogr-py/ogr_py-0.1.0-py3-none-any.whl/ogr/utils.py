"""Helper functions."""

def half(a: int) -> int:
    return a // 2

def div(a: int, b: int) -> int:
    return a // b

def dist(a: int, b: int) -> int:
    return abs(a - b)

def is_golomb_ruler(sequence: list[int]) -> bool:
    """Verify if a sequence of integers is a golomb ruler.

    In order for a sequence to be a golomb ruler, the differences between all items must be distinct
    """
    # first assert that all the elements are non-negative
    for el in sequence:
        if el < 0:
            return False

    differences = set()

    for (lhs_index, lhs) in enumerate(sequence):
        for rhs in sequence[(lhs_index + 1):]:

            difference = dist(lhs, rhs)
            # Check if the difference is distinct!
            if difference in differences:
                return False
            else:
                differences.add(difference)

    return True

def compute_distances(sequence: list[int]) -> set[int]:
    """Compute the pairwise distances of `sequence` and return the results in a set."""
    distances = set()

    for (lhs_index, lhs) in enumerate(sequence):
        for rhs in sequence[(lhs_index + 1):]:
            distances.add(dist(lhs, rhs))

    return distances