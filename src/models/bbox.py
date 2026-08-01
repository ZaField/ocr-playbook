from dataclasses import dataclass, field

@dataclass
class BBox:
    x1: float
    y1: float
    x2: float
    y2: float

    @classmethod
    def from_list(cls, box: list[float]) -> "BBox":
        return cls(*box)