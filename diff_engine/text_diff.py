from __future__ import annotations

from difflib import SequenceMatcher


def compare_text(old_lines: list[str], new_lines: list[str]) -> dict:
    """Line-level diff for text-like content."""
    matcher = SequenceMatcher(a=old_lines, b=new_lines)
    added: list[dict] = []
    deleted: list[dict] = []
    modified: list[dict] = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        if tag == "insert":
            for idx, line in enumerate(new_lines[j1:j2], start=j1 + 1):
                added.append({"line": idx, "content": line})
        elif tag == "delete":
            for idx, line in enumerate(old_lines[i1:i2], start=i1 + 1):
                deleted.append({"line": idx, "content": line})
        elif tag == "replace":
            old_chunk = old_lines[i1:i2]
            new_chunk = new_lines[j1:j2]
            max_len = max(len(old_chunk), len(new_chunk))
            for k in range(max_len):
                old_line = old_chunk[k] if k < len(old_chunk) else ""
                new_line = new_chunk[k] if k < len(new_chunk) else ""
                modified.append(
                    {
                        "old_line": i1 + k + 1 if old_line else None,
                        "new_line": j1 + k + 1 if new_line else None,
                        "old_content": old_line,
                        "new_content": new_line,
                    }
                )

    return {"added": added, "deleted": deleted, "modified": modified}
