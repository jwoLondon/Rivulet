import copy
import pytest
from interpreter import Interpreter

zeroes_glyph = """
╵ ╰──╮ ╭───╯╭──╯
╰─╮ ─┘ │╰─╮ └─ ╭─╮
  │╰──┐└─╴│╰───╯ │
  ╰─╮ ╰─╮ └─┐  ╭─╯
  ╶─┘   │ ╶─┘  ╰─╮  
      ╶─┘        │
                ─╯╷
"""

zeroes2_glyph = """
╵╵ ╰──╮ ╭───╯╭──╯
 ╰─╮ ─┘ │╰─╮ └─ ╭─╮
   │╰──┐└─╴│╰───╯ │
   ╰─╮ ╰─╮ └─┐  ╭─╯
   ╶─┘   │ ╶─┘  ╰─╮  
       ╶─┘        │
                 ─╯╷
"""

zeroes_glyph = [list(ln) for ln in zeroes_glyph.splitlines()] # format
zeroes_glyph = zeroes_glyph[1:] # remove first line

zeroes2_glyph = [list(ln) for ln in zeroes2_glyph.splitlines()] # format
zeroes2_glyph = zeroes2_glyph[1:] # remove first line

def test_shave_zeroes_1():
    intr = Interpreter()
    gl = copy.deepcopy(zeroes_glyph)
    glyph, level = intr._shave_glyph(gl)
    assert(glyph[0][0] == ' ')
    assert(glyph[-1][-1] == ' ')
    assert(level == 1)

def test_shave_zeroes_2():
    intr = Interpreter()
    gl = copy.deepcopy(zeroes2_glyph)
    glyph, level = intr._shave_glyph(gl)
    assert(glyph[0][0] == ' ')
    assert(glyph[-1][-1] == ' ')
    assert(level == 2)

#----
    
glyph_with_partial_start = """
╵ ╰──╮ ╷
╰─╮ ─┘ │╰─╮
  │╰──┐└─╴│
      │   ╷
"""

glyph_with_partial_start_bottom = """
╵ ╰──╮ ╮
╰─╮ ─┘ │╰─╮
  │╰──┐└─╴│
      ╵   ╷
"""

zeroes_prog_cmt = """
A COMMENT

 1 ╵ ╰──╮ ╭───╯╭──╯
 2 ╰─╮ ─┘ │╰─╮ └─ ╭─╮
 3   │╰──┐└─╴│╰───╯ │
 5   ╰─╮ ╰─╮ └─┐  ╭─╯
 7   ╶─┘   │ ╶─┘  ╰─╮  
11       ╶─┘        │
13                 ─╯╷

ANOTHER COMMENT"""

two_glyphs_prog = """
 1 ╵ ╰──╮ ╭───╯╭──╯     ╵╰──╮╶─╮ ╰╴╰─╮╭─┘
 2 ╰─╮ ─┘ │╰─╮ └─ ╭─╮      ─┘  ╰─╮╭──┘│
 3   │╰──┐└─╴│╰───╯ │          ╰─┘╰─╴ │   
 5   ╰─╮ ╰─╮ └─┐  ╭─╯              ───┘ ╷
 7   ╶─┘   │ ╶─┘  ╰─╮  
11       ╶─┘        │
13                 ─╯╷

"""

three_glyphs_prog = """
 1 ╵ ╰──╮ ╭───╯╭──╯     ╵╰──╮╶─╮ ╰╴╰─╮╭─┘
 2 ╰─╮ ─┘ │╰─╮ └─ ╭─╮      ─┘  ╰─╮╭──┘│
 3   │╰──┐└─╴│╰───╯ │          ╰─┘╰─╴ │   
 5   ╰─╮ ╰─╮ └─┐  ╭─╯              ───┘ ╷
 7   ╶─┘   │ ╶─┘  ╰─╮  
11       ╶─┘        │
13                 ─╯╷

╵╵╰──╮╰─╮╰─
    ─┘  │
    ────┘
      ╭
      │   ╷    
"""

zeroes_prog_cmt = [list(ln) for ln in zeroes_prog_cmt.splitlines()] # format
glyph_with_partial_start = [list(ln) for ln in glyph_with_partial_start.splitlines()] # format
glyph_with_partial_start_bottom = [list(ln) for ln in glyph_with_partial_start_bottom.splitlines()] # format
two_glyphs_prog = [list(ln) for ln in two_glyphs_prog.splitlines()] # format
three_glyphs_prog = [list(ln) for ln in three_glyphs_prog.splitlines()] # format

def test_locate_glyphs_zeroes():
    intr = Interpreter()
    gl = copy.deepcopy(zeroes_glyph)
    glyph_locs = intr._locate_glyphs(gl)
    assert(len(glyph_locs) == 1)
    assert(glyph_locs[0]['start'] == {"y": 0, "x": 0})
    assert(glyph_locs[0]['end'] == {"y": 6, "x": 18})

def test_locate_glyphs_zeroes():
    intr = Interpreter()
    gl = copy.deepcopy(zeroes_glyph)
    glyph_locs = intr._locate_glyphs(gl)
    assert(len(glyph_locs) == 1)
    assert(glyph_locs[0]['start'] == {"y": 0, "x": 0})
    assert(glyph_locs[0]['end'] == {"y": 6, "x": 18})    

def test_locate_glyphs_with_partial_start():
    intr = Interpreter()
    gl = copy.deepcopy(glyph_with_partial_start)
    glyph_locs = intr._locate_glyphs(gl)
    assert(len(glyph_locs) == 1)
    assert(glyph_locs[0]['start'] == {"y": 1, "x": 0})
    assert(glyph_locs[0]['end'] == {"y": 4, "x": 10})

def test_locate_glyphs_with_partial_start_bottom():
    intr = Interpreter()
    gl = copy.deepcopy(glyph_with_partial_start_bottom)
    glyph_locs = intr._locate_glyphs(gl)
    assert(len(glyph_locs) == 1)
    assert(glyph_locs[0]['start'] == {"y": 1, "x": 0})
    assert(glyph_locs[0]['end'] == {"y": 4, "x": 10})

def test_locate_glyphs_zeroes_comments():
    intr = Interpreter()
    pr = copy.deepcopy(zeroes_prog_cmt)
    glyph_locs = intr._locate_glyphs(pr)
    assert(len(glyph_locs) == 1)
    assert(glyph_locs[0]['start'] == {"y": 3, "x": 3})
    assert(glyph_locs[0]['end'] == {"y": 9, "x": 21})

def test_locate_two_glyphs():
    intr = Interpreter()
    pr = copy.deepcopy(two_glyphs_prog)
    glyph_locs = intr._locate_glyphs(pr)
    assert(len(glyph_locs) == 2)
    assert(glyph_locs[0]['start'] == {'y': 1, 'x': 3})
    assert(glyph_locs[0]['end'] == {'y': 7, 'x': 21})
    assert(glyph_locs[1]['start'] == {'y': 1, 'x': 24})
    assert(glyph_locs[1]['end'] == {'y': 4, 'x': 40})

def test_locate_three_glyphs():
    intr = Interpreter()
    pr = copy.deepcopy(three_glyphs_prog)
    glyph_locs = intr._locate_glyphs(pr)
    assert(len(glyph_locs) == 3)
    assert(glyph_locs[0]['start'] == {'y': 1, 'x': 3})
    assert(glyph_locs[0]['end'] == {'y': 7, 'x': 21})
    assert(glyph_locs[1]['start'] == {'y': 1, 'x': 24})
    assert(glyph_locs[1]['end'] == {'y': 4, 'x': 40})
    assert(glyph_locs[2]['start'] == {'y': 9, 'x': 0})
    assert(glyph_locs[2]['end'] == {'y': 13, 'x': 10})
