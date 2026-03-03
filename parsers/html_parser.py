from __future__ import annotations

from bs4 import BeautifulSoup

from core.document_model import DocumentObject
from parsers.common import read_text


def parse(path: str) -> DocumentObject:
    html = read_text(path)
    soup = BeautifulSoup(html, "html.parser")
    text_nodes = [t.strip() for t in soup.stripped_strings if t.strip()]
    return DocumentObject(type="text", content=text_nodes, metadata={"source": path})
