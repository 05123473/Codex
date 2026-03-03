from __future__ import annotations

from pathlib import Path

from core.document_model import DocumentObject
from parsers import code_parser, excel_parser, folder_parser, html_parser, ppt_parser, txt_parser, word_parser


def parse_input(path: str) -> DocumentObject:
    p = Path(path)
    if p.is_dir():
        return folder_parser.parse(path)

    ext = p.suffix.lower()
    if ext in {".txt", ".md", ".log"}:
        return txt_parser.parse(path)
    if ext in {".html", ".htm"}:
        return html_parser.parse(path)
    if ext in {".docx"}:
        return word_parser.parse(path)
    if ext in {".xlsx"}:
        return excel_parser.parse(path)
    if ext in {".pptx"}:
        return ppt_parser.parse(path)

    # fallback: treat as code/text
    return code_parser.parse(path)
