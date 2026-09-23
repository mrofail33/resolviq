from io import BytesIO
from pypdf import PdfReader


def extract_text_from_upload(filename: str, content: bytes) -> str:
    if filename.lower().endswith(".pdf"):
        return extract_pdf_text(content)
    return content.decode("utf-8", errors="ignore")


def extract_pdf_text(content: bytes) -> str:
    reader = PdfReader(BytesIO(content))
    pages = [page.extract_text() or "" for page in reader.pages]
    text = "\n".join(page.strip() for page in pages if page.strip())
    if not text:
        raise ValueError("No readable text found in PDF.")
    return text
