import tempfile
import os
import requests
import urllib3
import fitz  # PyMuPDF
from config import HEADERS, PDF_MAX_PAGES

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def download_pdf(pdf_url: str) -> str | None:
    if not pdf_url:
        return None
    try:
        resp = requests.get(pdf_url, headers=HEADERS, timeout=30, stream=True, verify=False)
        resp.raise_for_status()
        suffix = ".pdf"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
            return f.name
    except Exception as e:
        print(f"  [PDF 다운로드 실패] {pdf_url}: {e}")
        return None


def extract_text(pdf_path: str) -> str:
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for i, page in enumerate(doc):
            if i >= PDF_MAX_PAGES:
                break
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"  [PDF 추출 실패] {pdf_path}: {e}")
    return text.strip()


def get_report_text(pdf_url: str) -> str:
    path = download_pdf(pdf_url)
    if not path:
        return ""
    try:
        return extract_text(path)
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else ""
    if not url:
        print("사용법: python pdf_extractor.py <PDF_URL>")
        sys.exit(1)
    text = get_report_text(url)
    print(f"추출된 텍스트 ({len(text)}자):")
    print(text[:500])
