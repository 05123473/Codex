from __future__ import annotations

import hashlib
from pathlib import Path

from core.document_model import DocumentObject


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def parse(path: str) -> DocumentObject:
    root = Path(path)
    mapping: dict[str, str] = {}
    for file in root.rglob("*"):
        if file.is_file():
            rel = str(file.relative_to(root)).replace("\\", "/")
            mapping[rel] = _sha256(file)
    return DocumentObject(type="tree", content=mapping, metadata={"source": path})
