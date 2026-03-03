from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from core.document_model import DocumentObject
from diff_engine.table_diff import compare_table
from diff_engine.text_diff import compare_text
from diff_engine.tree_diff import compare_tree
from parsers.router import parse_input

app = FastAPI(title="Universal File Diff Tool", version="1.0.0")


class CompareRequest(BaseModel):
    fileA: str
    fileB: str


def _run_diff(a: DocumentObject, b: DocumentObject) -> dict:
    if a.type != b.type:
        raise HTTPException(status_code=400, detail=f"Type mismatch: {a.type} vs {b.type}")

    if a.type == "text":
        return compare_text(a.content, b.content)
    if a.type == "table":
        return compare_table(a.content, b.content)
    if a.type == "tree":
        return compare_tree(a.content, b.content)

    raise HTTPException(status_code=400, detail=f"Unsupported type: {a.type}")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/compare")
def compare(req: CompareRequest) -> dict:
    left = parse_input(req.fileA)
    right = parse_input(req.fileB)
    result = _run_diff(left, right)
    return {
        "left": {"type": left.type, "metadata": left.metadata},
        "right": {"type": right.type, "metadata": right.metadata},
        "diff_result": result,
    }
