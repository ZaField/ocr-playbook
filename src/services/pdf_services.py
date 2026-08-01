import fitz

from src.models.bbox import BBox
from src.models.page_results import PageResult
from src.models.region import Region
from src.utils.file_utils import base_name, ensure_dir

class PdfConverter:
    def __init__(self, dpi: int = 200):
        self.dpi = dpi

    def to_images(self, pdf_path: str, out_dir: str = "pdf_pages") -> list[str]:
        ensure_dir(out_dir)
        doc = fitz.open(pdf_path)
        zoom = self.dpi / 72
        mat = fitz.Matrix(zoom, zoom)
        name = base_name(pdf_path)

        paths = []
        for i, page in enumerate(doc):
            pix = page.get_pixmap(matrix=mat)
            out_path = f"{out_dir}/{name}_page{i+1}.png"
            pix.save(out_path)
            paths.append(out_path)
        return paths

    def is_text_based(self, pdf_path: str, min_chars: int = 20) -> bool:
        doc = fitz.open(pdf_path)
        for page in doc:
            if len(page.get_text().strip()) > min_chars:
                return True
        return False

    def extract_text_pages(self, pdf_path: str) -> list[PageResult]:
        """Extract native text directly, skipping OCR. Uses blocks to
        approximate reading order + rough region typing (title vs text)."""
        doc = fitz.open(pdf_path)
        page_results = []

        for page_num, page in enumerate(doc, start=1):
            blocks = page.get_text("dict")["blocks"]
            regions = []

            for block in blocks:
                if block.get("type") != 0:
                    continue

                block_text_lines = []
                font_sizes = []

                for line in block.get("lines", []):
                    line_text = "".join(span["text"] for span in line["spans"])
                    if line_text.strip():
                        block_text_lines.append(line_text)
                        font_sizes.extend(span["size"] for span in line["spans"])

                if not block_text_lines:
                    continue

                text = "\n".join(block_text_lines)
                x0, y0, x1, y1 = block["bbox"]
                avg_font_size = sum(font_sizes) / len(font_sizes) if font_sizes else 0

                # heuristic: larger font + short single line => likely a title/header
                region_type = "title" if (avg_font_size > 13 and len(block_text_lines) == 1) else "text"

                regions.append(Region(
                    type=region_type,
                    bbox=BBox(x0, y0, x1, y1),
                    text=text,
                ))

            try:
                tabs = page.find_tables()
                for tab in tabs.tables:
                    html = tab.to_pandas().to_html(index=False)
                    x0, y0, x1, y1 = tab.bbox
                    regions.append(Region(
                        type="table",
                        bbox=BBox(x0, y0, x1, y1),
                        html=html,
                    ))
            except Exception:
                pass 

            page_results.append(PageResult(
                source_path=pdf_path,
                page_number=page_num,
                regions=regions,
            ))

        return page_results