import os

from paddleocr import PaddleOCR

from src.models.bbox import BBox
from src.models.page_results import PageResult
from src.models.region import Region

class OcrService:
    def __init__(self, lang: str = "en", **kwargs):
        kwargs.setdefault("use_doc_orientation_classify", False)
        kwargs.setdefault("use_doc_unwarping", False)
        kwargs.setdefault("use_textline_orientation", False)
        kwargs.setdefault("enable_mkldnn", True)
        kwargs.setdefault("text_detection_model_name", "PP-OCRv6_medium_det")
        kwargs.setdefault("text_recognition_model_name", "PP-OCRv6_medium_rec")
        kwargs.setdefault("engine", "onnxruntime")
        self._engine = PaddleOCR(lang=lang, cpu_threads=os.cpu_count(), **kwargs)

    def analyze(self, image_path: str, page_number: int = 1) -> PageResult:
        output = self._engine.predict(image_path)

        regions = []
        for res in output:
            texts = res.get("rec_texts", [])
            boxes = res.get("rec_boxes", [])
            scores = res.get("rec_scores", [])

            for text, box, score in zip(texts, boxes, scores):
                x_coords = box[0::2] if len(box) > 4 else [box[0], box[2]]
                y_coords = box[1::2] if len(box) > 4 else [box[1], box[3]]
                bbox = BBox(min(x_coords), min(y_coords), max(x_coords), max(y_coords))

                regions.append(Region(
                    type="text",
                    bbox=bbox,
                    text=text,
                    confidence=float(score),
                ))
        page = PageResult(source_path=image_path, page_number=page_number, regions=regions)
        page.build_full_text()
        return page