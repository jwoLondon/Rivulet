import copy
import pytest
from interpreter import Interpreter

zeroes_st_glyph = """
  ╰──╮ ╭───╯╭──╯
╰─╮ ─┘ │╰─╮ └─ ╭─╮
  │╰──┐└─╴│╰───╯ │
  ╰─╮ ╰─╮ └─┐  ╭─╯
  ╶─┘   │ ╶─┘  ╰─╮  
      ╶─┘        │
                ─╯
"""
zeroes_st_glyph = [list(ln) for ln in zeroes_st_glyph.splitlines()] # format
zeroes_st_glyph = zeroes_st_glyph[1:] # remove first line

def test_find_starts():
    intr = Interpreter()
    gl = copy.deepcopy(zeroes_st_glyph)
    starts = intr._find_strand_starts(gl)
    assert(len(starts) == 7)
    assert(all(s["type"] == "data" for s in starts))
    assert(starts[0]["x"] == 2)
    assert(starts[0]["y"] == 0)
    assert(starts[1]["x"] == 11)
    assert(starts[1]["y"] == 0)
    assert(starts[2]["x"] == 15)
    assert(starts[2]["y"] == 0)
    assert(starts[3]["x"] == 0)
    assert(starts[3]["y"] == 1)
    assert(starts[4]["x"] == 8)
    assert(starts[4]["y"] == 1)
    assert(starts[5]["x"] == 3)
    assert(starts[5]["y"] == 2)
    assert(starts[6]["x"] == 11)
    assert(starts[6]["y"] == 2)

fib_2_glyph = """
╵╵╭─╶ ╮  ╭─┘╭─╶ 
  │   │╭─┘╭─╯  
  │╶╮ │╰─ │ 
  ╰─┘ ╰───┘
    ╮
    │   
"""

fib_2_glyph = [list(ln) for ln in fib_2_glyph.splitlines()] # format
fib_2_glyph = fib_2_glyph[1:] # remove first line

def test__find_starts_w_ends():
    intr = Interpreter()
    gl = copy.deepcopy(fib_2_glyph)
    starts = intr._find_strand_starts(gl)
    print(starts)