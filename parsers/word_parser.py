from __future__ import annotations

from docx import Document

from core.document_model import DocumentObject


def parse(path: str) -> DocumentObject:
    doc = Document(path)
    lines = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return DocumentObject(type="text", content=lines, metadata={"source": path})
