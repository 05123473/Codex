from __future__ import annotations


def compare_tree(tree1: dict[str, str], tree2: dict[str, str]) -> dict:
    """Diff two path->hash trees."""
    keys1 = set(tree1)
    keys2 = set(tree2)

    added = sorted(keys2 - keys1)
    deleted = sorted(keys1 - keys2)
    changed = sorted(k for k in (keys1 & keys2) if tree1[k] != tree2[k])

    return {"added": added, "deleted": deleted, "changed": changed}
