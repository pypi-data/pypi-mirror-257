"""Encoding of the different solvers available for use inside AMPL.

For an exhaustive list, consult: https://dev.ampl.com/solvers/index.html"""

from enum import Enum

class AMPLSolver(Enum):
    """Python Enum to rep"""

    CPLEX = 1

    def ampl_name(self) -> str:
        """Return a string representation of this solver that is used inside AMPL source code."""
        if self == AMPLSolver.CPLEX:
            return "cplex"