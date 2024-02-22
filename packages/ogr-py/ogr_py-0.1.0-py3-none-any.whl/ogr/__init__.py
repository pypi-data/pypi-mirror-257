"""Module that facilitates the solving of OGR instances using AMPL."""

from .models import *
from .generation import generate_golomb_ruler_improved, generate_golomb_ruler_naive
from .ruler import GolombRuler