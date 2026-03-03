from diff_engine.table_diff import compare_table
from diff_engine.text_diff import compare_text
from diff_engine.tree_diff import compare_tree


def test_text_diff_modified():
    res = compare_text(["a", "b"], ["a", "c"])
    assert res["modified"]


def test_table_diff_changed_cell():
    res = compare_table([["1", "2"]], [["1", "3"]])
    assert res["changed_cells"][0]["old"] == "2"
    assert res["changed_cells"][0]["new"] == "3"


def test_tree_diff_changed_and_added_deleted():
    a = {"a.txt": "x", "b.txt": "y"}
    b = {"b.txt": "z", "c.txt": "n"}
    res = compare_tree(a, b)
    assert res["added"] == ["c.txt"]
    assert res["deleted"] == ["a.txt"]
    assert res["changed"] == ["b.txt"]
