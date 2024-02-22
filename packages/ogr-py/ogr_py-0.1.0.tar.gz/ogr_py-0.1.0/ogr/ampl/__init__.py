"""A colllection of the different formulations needed to solve OGR."""

from ..solvers import *

def ampl_choose_solver(solver: AMPLSolver) -> str:
    """Return the AMPL source code that sets the solver to `solver`."""
    return (
        f"""
        option solver {solver.ampl_name()};
        solve;
        display d;
        """
    )

def ogr_integer_lp_model(order: int, upper_bound: int) -> str:
    """Return the ampl source code defining the integere linear programming formulation of OGR."""
    return (
        f"""
        param upper_bound = {upper_bound};
        param order = {order};
        """

        +

        """
        set N = {1..order};
        set V = {1..upper_bound};
        set pairs = {i in N, j in (i + 1)..order};
        set pairs_consecutive = {i in 1..order - 1, j in (i + 1)..order};

        var d {pairs} >= 1;
        var e {pairs, V} binary;

        minimize total_length: d[1, order];
        subject to distance_assignment {(i, j) in pairs}:
            sum{v in V} e[i, j, v] = 1;
        subject to distance_uniqueness {v in V}:
            sum {(i, j) in pairs} e[i, j, v] <= 1;
        subject to distance_definition {(i, j) in pairs}:
            sum {v in V} v * e[i, j, v] = d[i, j];
        subject to distance_identity {(i, j) in pairs_consecutive}:
            sum {k in i..j - 1} d[k, k + 1] = d[i, j];
        """
    )


def ogr_integer_lp(order: int, upper_bound: int, solver: AMPLSolver) -> str:
    """Return the complete ampl source code that loads an instance and solves """
    return (
        ogr_integer_lp_model(order, upper_bound) +
        ampl_choose_solver(solver)
    )