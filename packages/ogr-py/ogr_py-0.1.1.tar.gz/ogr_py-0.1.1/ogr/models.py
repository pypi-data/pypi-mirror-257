"""Module that facilities the automatic generation and execution of OGR models using ampl."""
from __future__ import annotations

from appdirs import user_data_dir
from collections.abc import Callable
from enum import Enum
from os.path import join, exists
from os import makedirs, remove
from random import randint
from shutil import which
import time
import subprocess

from .exceptions import AMPLNotFound, NotGolombRuler, SolveError
from .ruler import GolombRuler
from .ampl import ogr_integer_lp
from .solvers import AMPLSolver
# First check if ampl exists on this machine
_AMPL_PATH = which("ampl")
if _AMPL_PATH is None:
    raise AMPLNotFound

if __name__ == '__main__':
    full_path = which("ampl")
    full_path_fail = which("fake_executable")

class Formulations(Enum):
    """Class to represent the different formulations presented in our paper."""
    IntegerLinearProgram = 1
    IntegerLinearProgramRelaxation = 2
    ConstraintProgram = 3
    QuadraticProgram = 4

    def callback(self) -> Callable[[int, int, AMPLSolver], str]:
        """Return the function that generates the AMPL source code implementing this formulation."""
        if self == Formulations.IntegerLinearProgram:
            return ogr_integer_lp

    def from_str(input: str) -> Formulations:
        """Raises `ValueError` on bad input."""
        input = input.lower()
        if input == "ilp":
            return Formulations.IntegerLinearProgram
        elif input == "ilpr":
            return Formulations.IntegerLinearProgramRelaxation
        elif input == "cp":
            return Formulations.ConstraintProgram
        elif input == "qp":
            return Formulations.QuadraticProgram
        else:
            raise ValueError





def solve(order: int, upper_bound: int = None, formulation = Formulations.IntegerLinearProgram, solver: AMPLSolver = AMPLSolver.CPLEX, timeout_s: float = 60, verbose=False) -> GolombRuler:
    """Attempt to solve an instance of the OGR with `order` marks and """
    if upper_bound is None:
        upper_bound = 2 ** (order - 1) - 1

    if verbose:

        print(f"============> OGR Solve ================>")
        print(f"=> order:       {order}")
        print(f"=> formulation: {formulation.name}")
        print(f"=> solver:      {solver.name}")
        # print(f"=> timeout:     {int(timeout_s)}s")


    # Build the temporary source code for an AMPL script
    ampl_source_code_callback = formulation.callback()
    source_code = ampl_source_code_callback(order, upper_bound, solver)

    # Store the file in a temporary location
    data_dir = user_data_dir("ogr", "ejovo")
    if not exists(data_dir):
        makedirs(data_dir)

    tmp_file = join(data_dir, f"tmp_{randint(1, 99999):08}.ampl")
    with open(tmp_file, "w") as file:
        file.write(source_code)


    # Now actually run our model
    arguments = [_AMPL_PATH, tmp_file]
    start = time.time()
    output = subprocess.run(arguments, capture_output=True, timeout=timeout_s)
    solved = output.stdout.decode()
    end = time.time()

    # Now let's process the output and turn the distances into a GolombRuler.
    # Find the line that has "d :="   lines = solved.split("\n")
    try:
        lines = solved.split("\n")
        index = lines.index("d :=")

        # Now only consider the next (order - 1) lines
        distances = lines[(index + 1):(index + order)]
        distances = [int(d.split()[-1]) for d in distances]

        ruler = GolombRuler.from_distances(distances, order)

    except NotGolombRuler as ngr:

        raise SolveError(f"Error when processing problem with order {order} and upper_bound: {upper_bound}. AMPL output: {solved} AMPL source code: {source_code}")

    except:

        # raise SolveError(solved)
        remove(tmp_file)
        return GolombRuler([0])

    # Remove the tmp file
    remove(tmp_file)

    return ruler
