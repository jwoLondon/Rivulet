# pylint: skip-file
"""
Test glyph locating and separation
"""
import copy
import pytest
from riv_parser import Parser

zeroes_glyph = """
╵ ╰──╮ ╭───╯╭──╯
╰─╮ ─┘ │╰─╮ └─ ╭─╮
  │╰──┐└─╴│╰───╯ │
  ╰─╮ ╰─╮ └─┐  ╭─╯
  ╶─┘   │ ╶─┘  ╰─╮  
      ╶─┘        │
                ─╯╷
"""
zeroes_glyph = [list(ln) for ln in zeroes_glyph.splitlines()] # format

def test_shave_zeroes_1st_level():
    intr = Parser()
    gl = copy.deepcopy(zeroes_glyph)
    gl = intr._remove_blank_lines(gl)
    glyph_locs = intr._locate_glyphs(gl)
    block_tree = intr._prepare_glyphs_for_lexing(glyph_locs, gl)
    assert(block_tree[0]["glyph"][0][0] == ' ')
    assert(block_tree[0]["glyph"][-1][-1] == ' ')
    assert(block_tree[0]["level"] == 1)

zeroes2_glyph = """
╵╵ ╰──╮ ╭───╯╭──╯
 ╰─╮ ─┘ │╰─╮ └─ ╭─╮
   │╰──┐└─╴│╰───╯ │
   ╰─╮ ╰─╮ └─┐  ╭─╯
   ╶─┘   │ ╶─┘  ╰─╮  
       ╶─┘        │
                 ─╯╷
"""
zeroes2_glyph = [list(ln) for ln in zeroes2_glyph.splitlines()] # format

def test_shave_zeroes_2nd_level():
    intr = Parser()
    gl = copy.deepcopy(zeroes2_glyph)
    gl = intr._remove_blank_lines(gl)
    glyph_locs = intr._locate_glyphs(gl)
    block_tree = intr._prepare_glyphs_for_lexing(glyph_locs, gl)
    assert(block_tree[0]["glyph"][0][0] == ' ')
    assert(block_tree[0]["glyph"][-1][-1] == ' ')
    assert(block_tree[0]["level"] == 2)

#----
    
glyph_with_partial_start = """
╵ ╰──╮ ╷
╰─╮ ─┘ │╰─╮
  │╰──┐└─╴│
      │   ╷
"""
glyph_with_partial_start = [list(ln) for ln in glyph_with_partial_start.splitlines()]

glyph_with_partial_start_bottom = """
╵ ╰──╮ ╮
╰─╮ ─┘ │╰─╮
  │╰──┐└─╴│
      ╵   ╷
"""
glyph_with_partial_start_bottom = [list(ln) for ln in glyph_with_partial_start_bottom.splitlines()]

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
zeroes_prog_cmt = [list(ln) for ln in zeroes_prog_cmt.splitlines()] # format

two_glyphs_prog = """
 1 ╵ ╰──╮ ╭───╯╭──╯     ╵╰──╮╶─╮ ╰╴╰─╮╭─┘
 2 ╰─╮ ─┘ │╰─╮ └─ ╭─╮      ─┘  ╰─╮╭──┘│
 3   │╰──┐└─╴│╰───╯ │          ╰─┘╰─╴ │   
 5   ╰─╮ ╰─╮ └─┐  ╭─╯              ───┘ ╷
 7   ╶─┘   │ ╶─┘  ╰─╮  
11       ╶─┘        │
13                 ─╯╷

"""
two_glyphs_prog = [list(ln) for ln in two_glyphs_prog.splitlines()] # format

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
three_glyphs_prog = [list(ln) for ln in three_glyphs_prog.splitlines()] # format

def test_locate_glyphs_zeroes():
    intr = Parser()
    gl = copy.deepcopy(zeroes_glyph)
    gl = intr._remove_blank_lines(gl)
    glyph_locs = intr._locate_glyphs(gl)
    assert(len(glyph_locs) == 1)
    assert(glyph_locs[0]['start'] == {"y": 0, "x": 0})
    assert(glyph_locs[0]['end'] == {"y": 6, "x": 18})

def test_locate_glyphs_with_partial_start():
    intr = Parser()
    gl = copy.deepcopy(glyph_with_partial_start)
    gl = intr._remove_blank_lines(gl)
    glyph_locs = intr._locate_glyphs(gl)
    assert(len(glyph_locs) == 1)
    assert(glyph_locs[0]['start'] == {"y": 0, "x": 0})
    assert(glyph_locs[0]['end'] == {"y": 3, "x": 10})

def test_locate_glyphs_with_partial_start_bottom():
    intr = Parser()
    gl = copy.deepcopy(glyph_with_partial_start_bottom)
    gl = intr._remove_blank_lines(gl)
    glyph_locs = intr._locate_glyphs(gl)
    assert(len(glyph_locs) == 1)
    assert(glyph_locs[0]['start'] == {"y": 0, "x": 0})
    assert(glyph_locs[0]['end'] == {"y": 3, "x": 10})

def test_locate_glyphs_zeroes_comments():
    intr = Parser()
    pr = copy.deepcopy(zeroes_prog_cmt)
    pr = intr._remove_blank_lines(pr)
    glyph_locs = intr._locate_glyphs(pr)
    assert(len(glyph_locs) == 1)
    assert(glyph_locs[0]['start'] == {"y": 2, "x": 3})
    assert(glyph_locs[0]['end'] == {"y": 8, "x": 21})

def test_locate_two_glyphs():
    intr = Parser()
    pr = copy.deepcopy(two_glyphs_prog)
    pr = intr._remove_blank_lines(pr)
    glyph_locs = intr._locate_glyphs(pr)
    assert(len(glyph_locs) == 2)
    assert(glyph_locs[0]['start'] == {'y': 0, 'x': 3})
    assert(glyph_locs[0]['end'] == {'y': 6, 'x': 21})
    assert(glyph_locs[1]['start'] == {'y': 0, 'x': 24})
    assert(glyph_locs[1]['end'] == {'y': 3, 'x': 40})

def test_prepare_two_glyphs():
    intr = Parser()
    pr = copy.deepcopy(two_glyphs_prog)
    pr = intr._remove_blank_lines(pr)
    glyph_locs = intr._locate_glyphs(pr)
    assert(len(glyph_locs) == 2)
    block_tree = intr._prepare_glyphs_for_lexing(glyph_locs, pr)
    assert(len(block_tree) == 2)

def test_locate_three_glyphs():
    intr = Parser()
    pr = copy.deepcopy(three_glyphs_prog)
    pr = intr._remove_blank_lines(pr)
    glyph_locs = intr._locate_glyphs(pr)
    assert(len(glyph_locs) == 3)
    assert(glyph_locs[0]['start'] == {'y': 0, 'x': 3})
    assert(glyph_locs[0]['end'] == {'y': 6, 'x': 21})
    assert(glyph_locs[1]['start'] == {'y': 0, 'x': 24})
    assert(glyph_locs[1]['end'] == {'y': 3, 'x': 40})
    assert(glyph_locs[2]['start'] == {'y': 8, 'x': 1})
    assert(glyph_locs[2]['end'] == {'y': 12, 'x': 10})

has_ref_at_end = """
╵╭─╶ ╮  ╭─┘╭─╶         
 │   │╭─┘╭─╯           
 │╶╮ │╰─ │             
 ╰─┘ ╰───┘
     ╮                 
   │ │         
   ╰─┘       ╷

"""
has_ref_at_end = [list(ln) for ln in has_ref_at_end.splitlines()] # format

def test_scan_glyph_with_ref_at_end():
    intr = Parser()
    pr = copy.deepcopy(has_ref_at_end)
    pr = intr._remove_blank_lines(pr)
    glyph_locs = intr._locate_glyphs(pr)
    assert(len(glyph_locs) == 1)

# Second level glyph
fib_2_glyph = """
╵╵╭─╶ ╮  ╭─┘╭─╶ 
  │   │╭─┘╭─╯  
  │╶╮ │╰─ │ 
  ╰─┘ ╰───┘
    ╮
    │         ╷
"""

fib_2_glyph = [list(ln) for ln in fib_2_glyph.splitlines()] # format
fib_2_glyph = fib_2_glyph[1:] # remove first line

def test_determine_level_2():
    intr = Parser()
    gl = copy.deepcopy(fib_2_glyph)
    gl = intr._remove_blank_lines(gl)
    glyph_locs = intr._locate_glyphs(gl)    
    assert(len(glyph_locs) == 1)
    assert(glyph_locs[0]['level'] == 2)

def test_determine_level_1():
    intr = Parser()
    gl = copy.deepcopy(has_ref_at_end)
    gl = intr._remove_blank_lines(gl)
    glyph_locs = intr._locate_glyphs(gl)    
    assert(len(glyph_locs) == 1)
    assert(glyph_locs[0]['level'] == 1)

# White space on top
whitespace_top_glyph = """



 ╵╭─╶ ╮  ╭─┘╭─╶ 
  │   │╭─┘╭─╯  
  │╶╮ │╰─ │ 
  ╰─┘ ╰───┘   ╷
"""

whitespace_top_glyph = [list(ln) for ln in whitespace_top_glyph.splitlines()] # format
whitespace_top_glyph = whitespace_top_glyph[1:] # remove first line

def test_clear_whitespace_top():
    intr = Parser()
    gl = copy.deepcopy(whitespace_top_glyph)
    gl = intr._remove_blank_lines(gl)
    glyph_locs = intr._locate_glyphs(gl)    
    assert(len(glyph_locs) == 1)

wide_with_uneven_lines = """
╵╰──╮╰─╮╷╰─╮╭─╮
 ╭─╮│ ─┘│ ─┘│ │
 │ ╰────┘ ╭─┘ │
 ╷   ╭────┘   │
 ╰───┘        ╰────────────────────────────────────────────╷
"""

wide_with_uneven_lines = [list(ln) for ln in wide_with_uneven_lines.splitlines()] # format
wide_with_uneven_lines = wide_with_uneven_lines[1:] # remove first line

def test_locate_glyph_with_uneven_lines():
    intr = Parser()
    gl = copy.deepcopy(wide_with_uneven_lines)
    gl = intr._remove_blank_lines(gl)
    glyph_locs = intr._locate_glyphs(gl)    
    assert(len(glyph_locs) == 1)
