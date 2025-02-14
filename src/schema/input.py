from typing import Any, Tuple, List
from enum import Enum

from pydantic import BaseModel


class FormatType(str, Enum):
    contours = "contours"
    colormerge = "colormerge"
    colormerge_forced = "colormerge_forced"
    combined = "combined"
    combined_forced = "combined_forced"
    mesh = "mesh"

class ColorType(str, Enum):
    default = "default"
    fifths = "fifths"
    fifthsv2 = "fifthsv2"

class Input(BaseModel):
    compactness: int = 5
    n_segments: int = 2000
    thresh: int = 50
    contour_color: Tuple[int, int, int] = (255,0,0)
    t_lower: int = 50
    t_upper: int = 130
    cont_thickness: int = 1
