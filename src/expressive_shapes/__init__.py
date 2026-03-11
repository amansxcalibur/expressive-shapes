from importlib.metadata import version

__version__ = version("expressive-shapes")

DEBUG = False

from .geometry.bezier_geometry import Point, Cubic
from .geometry.corner_rounding import CornerRounding, RoundedCorner
from .geometry.rounded_polygon import RoundedPolygon, Feature
from .geometry.polygon_measure import (
    MeasuredPolygon,
    MeasuredCubic,
    DoubleMapper,
)
from .morph.bezier_morph import Morph

__all__ = [
    "DEBUG",
    # geometry
    "Point",
    "Cubic",
    "CornerRounding",
    "RoundedCorner",
    "RoundedPolygon",
    "Feature",
    "MeasuredPolygon",
    "MeasuredCubic",
    "DoubleMapper",
    # morph
    "Morph",
]
