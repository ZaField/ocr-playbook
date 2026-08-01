from dataclasses import dataclass, field

from src.models.region import Region

@dataclass
class PageResult:
    source_path: str
    page_number: int
    regions: list[Region] = field(default_factory=list)
    full_text: str = ""

    def sorted_regions(self) -> list[Region]:
        return sorted(self.regions, key=lambda r: (r.bbox.y1, r.bbox.x1))

    def build_full_text(self) -> str:
        """Concatenate all region text/html in reading order into one string."""
        parts = []
        for r in self.sorted_regions():
            if r.type == "table" and r.html:
                parts.append(r.html)
            elif r.text:
                parts.append(r.text)
        self.full_text = "\n\n".join(parts)
        return self.full_text