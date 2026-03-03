from __future__ import annotations

from core.document_model import DocumentObject
from parsers.common import read_text


def parse(path: str) -> DocumentObject:
    return DocumentObject(type="text", content=read_text(path).splitlines(), metadata={"source": path})
