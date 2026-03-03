from __future__ import annotations


def compare_table(table1: list[list[str]], table2: list[list[str]]) -> dict:
    """Cell-level table diff by row/column indices."""
    changes: list[dict] = []
    max_rows = max(len(table1), len(table2))

    for r in range(max_rows):
        row1 = table1[r] if r < len(table1) else []
        row2 = table2[r] if r < len(table2) else []
        max_cols = max(len(row1), len(row2))
        for c in range(max_cols):
            v1 = row1[c] if c < len(row1) else ""
            v2 = row2[c] if c < len(row2) else ""
            if v1 != v2:
                changes.append(
                    {
                        "row": r + 1,
                        "col": c + 1,
                        "old": v1,
                        "new": v2,
                    }
                )

    return {"changed_cells": changes}
