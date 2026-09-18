# ocr-playbook (playground branch)

This branch is for testing and development only. It has no `src/` and no application code, just a `pyproject.toml` with the same OCR dependencies as the real project, plus Jupyter for interactive work.

Use this branch to try things out before they go anywhere near `development` or `production`: new PaddleOCR pipelines, table extraction approaches, parsing ideas, anything experimental. Nothing here needs to be clean, working, or permanent. If a piece of code proves out here, port it into `development` on purpose, do not build the real pipeline on this branch.

## Dependencies

- `paddleocr`, `paddlepaddle`, `paddlex[ocr]` for OCR and document structure parsing
- `pymupdf` for PDF handling
- `jupyter`, `ipykernel` for the notebook

## Setup

```bash
uv sync
```

This creates `.venv` and installs everything pinned in `uv.lock`.

## Working with the notebook

```bash
uv run jupyter notebook
```

Opens `starter.ipynb` in the browser with the project's environment already active.

To run it headless instead of interactively:

```bash
uv run jupyter nbconvert --to notebook --execute starter.ipynb
```
