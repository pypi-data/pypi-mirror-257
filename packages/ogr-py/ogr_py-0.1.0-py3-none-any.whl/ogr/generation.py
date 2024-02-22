"""Start exploring the GolombRuler problem.

A Golomb ruler is a sequence of non-negative integers such that every difference of two integers is distinct.

"""

from __future__ import annotations

from .exceptions import *
from .utils import compute_distances, dist


def generate_golomb_ruler_naive(order: int) -> list[int]:
    """Naively generate a new golomb ruler with `order` marks."""
    if order < 1: ValueError("order must be greater than 0")
    if order == 1: return [0]

    prev = generate_golomb_ruler_naive(order - 1)
    next = 2 ** (order - 1) - 1
    prev.append(next)

    return prev

def generate_golomb_ruler_improved(order: int) -> list[int]:
    """Generate a golomb ruler with order `order` using an improved algorithm.

    This algorithm runs in O(n^4)
    """
    if order < 1: ValueError("order must be greater than 0")
    if order == 1: return [0]
    if order == 2: return [0, 1]
    if order == 3: return [0, 1, 3]

    prev = generate_golomb_ruler_improved(order - 1)


    # Compute the differences
    distances = compute_distances(prev) # O(n^2)
    candidate_upper_bound = 2 * prev[-1] + 1 # Guarantees that we will accept at least one candidate

    def should_accept_candidate(candidate: int) -> bool:
        """Utility function used to check if a candidate should be accepted.

        Allows us to skip to the next loop on a false input (otherwise we only break from an inner loop)

        Runs in O(n)
        """
        for i in range(order - 1):
            if dist(candidate, prev[i]) in distances:
                return False

        return True

    for c in range(prev[-1], candidate_upper_bound + 1):
        # O(n) check to make sure that c != x_i for all i in 1..n
        # we could turn previous into a set to speed up this but that wouldn't
        # change asymptotic complexity
        if c in prev:
            continue

        if should_accept_candidate(c):
            prev.append(c)
            return sorted(prev)

    raise Exception("Implementation Error!!!")

# def main():

#     ruler = GolombRuler([0, 1, 3])
#     print(ruler)

#     ruler = GolombRuler(generate_golomb_ruler_improved(5))
#     print(ruler)

#     ruler_copy = GolombRuler.from_distances(ruler.triu_distances(), ruler.order())
#     print(ruler_copy)