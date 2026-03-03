from __future__ import annotations

from core.document_model import DocumentObject
from parsers.common import read_text


def parse(path: str) -> DocumentObject:
    text = read_text(path)
    return DocumentObject(type="text", content=text.splitlines(), metadata={"source": path})
