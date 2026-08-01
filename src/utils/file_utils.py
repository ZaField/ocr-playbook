import os

def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path

def base_name(path: str) -> str:
    return os.path.splitext(os.path.basename(path))[0]

def is_pdf(path: str) -> bool:
    return path.lower().endswith(".pdf")