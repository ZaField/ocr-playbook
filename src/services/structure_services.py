import os

from paddleocr import PPStructureV3

from src.models.bbox import BBox
from src.models.page_results import PageResult
from src.models.region import Region

class StructureService:
    def __init__(self, **kwargs):
        kwargs.setdefault("enable_mkldnn", True)
        kwargs.setdefault("use_textline_orientation", False)
        kwargs.setdefault("use_seal_recognition", False)
        kwargs.setdefault("use_formula_recognition", False)
        kwargs.setdefault("use_chart_recognition", False)
        kwargs.setdefault("cpu_threads", os.cpu_count())
        kwargs.setdefault("engine", "onnxruntime")
        self._pipeline = PPStructureV3(**kwargs)

    def analyze(self, image_path: str, page_number: int = 1) -> PageResult:
        output = self._pipeline.predict(input=image_path)

        regions = []
        for res in output:
            md_info = res.markdown
            regions.append(Region(
                type="text",
                bbox=BBox(0, 0, 0, 0),
                text=md_info.get("markdown_texts", ""),
            ))

        page = PageResult(source_path=image_path, page_number=page_number, regions=regions)
        page.build_full_text()
        return page

    def analyze_to_markdown(self, image_path: str) -> str:
        output = self._pipeline.predict(input=image_path)
        markdown_list = [res.markdown for res in output]
        return self._pipeline.concatenate_markdown_pages(markdown_list)