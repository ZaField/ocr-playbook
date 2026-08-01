from dataclasses import dataclass
from typing import Literal

from src.models.bbox import BBox

RegionType = Literal[
    "title", "text", "table", "figure", "figure_caption",
    "header", "footer", "reference", "equation"
]

@dataclass
class Region:
    type: RegionType
    bbox: BBox
    text: str = ""          # plain text content (non-table regions)
    html: str = ""          # table HTML (table regions only)
    confidence: float | None = None