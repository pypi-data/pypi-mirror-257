"""Functions that are designed to be entry points to `poetry run`."""

from argparse import ArgumentParser
from .exceptions import *
from . import models

def solve():
    """Script to launch our AMPL model to solve for an optimal ruler."""

    parser = ArgumentParser()

    parser.add_argument("order", help="The number of marks on our GolombRuler", type=int)
    parser.add_argument("--verbose", help="Print additional information about the solving process", action="store_true")
    parser.add_argument("--formulation", help="Which formulation of the problem we should use. Must be in ['ilp', 'ilpr', 'cp', 'qp']", default='ilp')
    parser.add_argument("--upper-bound", help="Upper bound for Integer Linear Programming formulation.", default=None, type=int)

    args = parser.parse_args()

    if args.order > 10:
        raise OrderTooLarge("Consider using an order less than 10..")

    try:
        formulation = models.Formulations.from_str(args.formulation)
    except:
        print(f"Oops! Problem formulation: '{args.formulation}' not recognized! Possible values: {{'ilp', 'ilpr', 'cp', 'qp'}}")
        exit

    ruler = models.solve(args.order, args.upper_bound, formulation, verbose=args.verbose)