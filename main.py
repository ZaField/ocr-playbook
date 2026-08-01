import sys
import time

from src.services.ocr_services import OcrService
from src.services.pdf_services import PdfConverter
from src.services.structure_services import StructureService
from src.utils.file_utils import base_name, ensure_dir, is_pdf
from src.utils.markdown_utils import page_to_markdown
from src.utils.logger import get_logger

import warnings
warnings.filterwarnings("ignore")

logger = get_logger()

def process_file(path: str, output_dir: str = "outputs", dpi: int = 200):
    run_start = time.perf_counter()
    ensure_dir(output_dir)
    converter = PdfConverter(dpi=dpi)

    if is_pdf(path) and converter.is_text_based(path):
        logger.info(f"{path} is text-based — extracting directly, skipping OCR.")
        t0 = time.perf_counter()
        page_results = converter.extract_text_pages(path)
        logger.info(f"Text extraction took {time.perf_counter() - t0:.2f}s")

    else:
        structure = OcrService()
        if is_pdf(path):
            image_paths = converter.to_images(path, out_dir=f"{output_dir}/pages")
        else:
            image_paths = [path]
            logger.info(f"PDF-to-image conversion took {time.perf_counter() - t0:.2f}s "
                    f"({len(image_paths)} page(s))")

        page_results = []
        for i, img_path in enumerate(image_paths, start=1):
            t_page = time.perf_counter()
            page_results.append(structure.analyze(img_path, page_number=i))
            logger.info(f"OCR page {i} took {time.perf_counter() - t_page:.2f}s")

    t0 = time.perf_counter()
    for page in page_results:
        md = page_to_markdown(page)
        out_path = f"{output_dir}/{base_name(path)}_page{page.page_number}_structured.md"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(md)
        logger.info(f"Saved {out_path}")

        txt_path = f"{output_dir}/{base_name(path)}_page{page.page_number}_fulltext.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(page.full_text)
        logger.info(f"Saved {txt_path}")

    logger.info(f"File writing took {time.perf_counter() - t0:.2f}s")
    logger.info(f"Total run time for {path}: {time.perf_counter() - run_start:.2f}s")

if __name__ == "__main__":
    file_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "outputs"
    process_file(file_path, output_dir=output_dir)