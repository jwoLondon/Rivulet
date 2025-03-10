# pylint: skip-file
"""
Test glyph full parsing
"""
import copy
import pytest
from riv_interpreter import Interpreter

def test_treeify_1_3_3():
    set_one = [
        {'level': 1},
        {'level': 3},
        {'level': 3},
    ]

    int = Interpreter()
    tree = int.treeify_glyphs(set_one, 1, [])
    assert len(tree) == 2
    assert isinstance(tree[1], list)
    assert len(tree[1]) == 1
    assert isinstance(tree[1][0], list)
    assert len(tree[1][0]) == 2

def test_treeify_1_3_2_2_3_3_1():
    set_one = [
        {'level': 1},
        {'level': 3},
        {'level': 2},
        {'level': 2},
        {'level': 3},
        {'level': 3},
        {'level': 1},
    ]

    int = Interpreter()
    tree = int.treeify_glyphs(set_one, 1, [])
    assert len(tree) == 3
    assert not isinstance(tree[0], list)
    assert isinstance(tree[1], list)
    assert not isinstance(tree[2], list)

    assert isinstance(tree[1][0], list)
    assert not isinstance(tree[1][1], list)
    assert not isinstance(tree[1][2], list)
    assert isinstance(tree[1][3], list)

    assert len(tree[1][0]) == 1
    assert len(tree[1][3]) == 2