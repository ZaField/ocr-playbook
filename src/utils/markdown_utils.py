from src.models.page_results import PageResult
from src.models.region import Region


def region_to_markdown(region: Region) -> str:
    if region.type == "table":
        return f"\n{region.html}\n"

    if region.type in ("figure", "figure_caption"):
        bbox = region.bbox
        return f"\n*[figure region, bbox: ({bbox.x1}, {bbox.y1}, {bbox.x2}, {bbox.y2})]*\n"

    if region.type == "title":
        return f"\n## {region.text}\n"

    return f"\n{region.text}\n"

def page_to_markdown(page: PageResult) -> str:
    parts = [region_to_markdown(r) for r in page.sorted_regions()]
    return "".join(parts).strip()