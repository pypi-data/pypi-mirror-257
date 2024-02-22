"""Definition of the `GolombRuler` class."""

from __future__ import annotations

from .generation import *
from .utils import *
from .exceptions import NotGolombRuler

class GolombRuler:
    """A list of non-negative integers such that each pairwise difference is distinct."""

    def __init__(self, sequence: list[int], assert_golomb_property = True):
        """Construct a new GolombRuler.

        Raises `NotGolombRuler` if the input sequence is malformed.
        """
        if assert_golomb_property:
            if not is_golomb_ruler(sequence):
                raise NotGolombRuler(f"Input sequence: {sequence} does not satisfy the GolombRuler conditions.")

        self.sequence = sequence

    def __str__(self) -> str:
        s = "GolombRuler {\n"
        s += f"  order:\t{self.order()}\n"
        s += f"  sequence:\t{self.sequence}\n"
        s += f"  distances:\t{self.triu_distances()}\n"
        s += f"  length:\t{self.length()}\n"
        s += "}"

        return s

    def order(self) -> int:
        """Return the order (number of elements in the sequence) of this GolombRuler."""
        return len(self.sequence)

    def length(self) -> int:
        """The largest distance of our GolombRuler. To return the number of elements, see `GolombRuler.order`."""
        return max(self.sequence)


    def d_plus_e(self) -> str:
        """Return a string representation of the d plus e model."""


    # ---------------------------------------------------------------------------- #
    #               Functions dealing with upper triangular matrices               #
    # ---------------------------------------------------------------------------- #
    def triu_size(self) -> int:
        """Compute the amount of space needed for a 1-dimensional matrix that encodes the distances between all pairs of marks."""
        n = self.order()
        return n * (n - 1) // 2

    def triu_elements_before_row(self, row_index: int) -> int:
        """Compute the number of elements before our 0-based indexing row.

        Consider the following upper triangular matrix containing the distances between marks in a 3-order golomb ruler:
        ```
        i: 0    |   -     d_12    d_13    |
        i: 1    |   -      -      d_23    |
        i: 2    |   -      -        -     |
        ```

        `triu_elements_before_row` computes the number of elements before a certain row. For example,
        we expect `triu_elements_before_row(1)` -> 2 and `triu_elements_before_row(2)` -> 3

        This function is used to compute the appropriate index for an array encoding the distances between marks.
        """
        n = self.order()
        i = row_index + 1
        return -half(i * i) + half(i * (2 * n + 1)) - n

    def triu_linear_index(self, row_index: int, col_index: int) -> int:
        """Compute the linear index for a upper triangular coordinate."""
        return self.triu_elements_before_row(row_index) + col_index

    def triu_distances(self) -> list[int]:
        """Compute the distances between every mark of this ruler, storing the results in a 1-d list."""
        distances: list[int] = [0 for _ in range(self.triu_size())]
        idx = 0

        for (lhs_idx, lhs) in enumerate(self.sequence):
            for rhs in self.sequence[(lhs_idx + 1):]:
                distances[idx] = dist(lhs, rhs)
                idx += 1

        return distances

    # ---------------------------------------------------------------------------- #
    #                                Static Methods                                #
    # ---------------------------------------------------------------------------- #
    @staticmethod
    def from_distances(distances: list[int], order: int) -> GolombRuler:
        """Construct a new GolombRuler given a list of distances.

        Used to read the output of the linear programming formulation.
        """
        # Assume that the first mark is 0.
        marks = [0]
        marks.extend(distances[:(order - 1)])
        return GolombRuler(marks)

    @staticmethod
    def generate_naive(order: int) -> GolombRuler:
        return GolombRuler(generate_golomb_ruler_naive(order), assert_golomb_property=False)

    @staticmethod
    def generate_improved(order: int) -> GolombRuler:
        return GolombRuler(generate_golomb_ruler_improved(order), assert_golomb_property=False)
