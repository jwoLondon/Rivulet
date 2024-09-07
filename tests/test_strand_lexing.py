# pylint: skip-file
"""
Test strand analysis in lexer
"""
import copy
import pytest
from lexer import Lexer

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

def test_find_starts_data_strands():
    "Find the start of every strand"
    intr = Lexer()
    gl = copy.deepcopy(zeroes_st_glyph)
    starts = intr._find_strand_starts(gl)
    assert len(starts) == 7
    assert all(s["type"] == "data" for s in starts)
    assert starts[0]["x"] == 2
    assert starts[0]["y"] == 0
    assert starts[1]["x"] == 11
    assert starts[1]["y"] == 0
    assert starts[2]["x"] == 15
    assert starts[2]["y"] == 0
    assert starts[3]["x"] == 0
    assert starts[3]["y"] == 1
    assert starts[4]["x"] == 8
    assert starts[4]["y"] == 1
    assert starts[5]["x"] == 3
    assert starts[5]["y"] == 2
    assert starts[6]["x"] == 11
    assert starts[6]["y"] == 2

def test_lex_zeroes():
    "Test each strand is a value strand with value 0"
    intr = Lexer()
    gl = [{"glyph": copy.deepcopy(zeroes_st_glyph)}]
    intr._load_primes(gl)
    starts = intr.lex_glyph(gl[0]["glyph"])
    for s in starts:
      assert s["type"] == "data"
      assert s["subtype"] == "value"
      assert s["value"] == 0

glyph_with_ref_strand_vert = """
╰──╮
   │
   ╷
"""
glyph_with_ref_strand_vert = [list(ln) for ln in glyph_with_ref_strand_vert.splitlines()] # format
glyph_with_ref_strand_vert = glyph_with_ref_strand_vert[1:] # remove first line

def test_glyph_with_ref_strand_vert():
    "Test a glyph with an action element strand"
    intr = Lexer()
    gl = [{"glyph": copy.deepcopy(glyph_with_ref_strand_vert)}]
    intr._load_primes(gl)
    starts = intr.lex_glyph(gl[0]["glyph"])
    assert len(starts) == 1
    assert starts[0]["type"] == "data"
    assert starts[0]["subtype"] == "ref"
    assert starts[0]["x"] == 0
    assert starts[0]["y"] == 0
    assert starts[0]["end_x"] == 3
    assert starts[0]["end_y"] == 2


glyph_with_action_strand = """
╰──╮╰─╮╰─╮
   │ ─┘  │
     ────┘
      ╭
      │
      │
"""
glyph_with_action_strand = [list(ln) for ln in glyph_with_action_strand.splitlines()] # format
glyph_with_action_strand = glyph_with_action_strand[1:] # remove first line

def test_identify_action_element_strand():
    "Test a glyph with an action element strand"
    intr = Lexer()
    gl = [{"glyph": copy.deepcopy(glyph_with_action_strand)}]
    intr._load_primes(gl)
    starts = intr.lex_glyph(gl[0]["glyph"])
    assert len(starts) == 4
    assert starts[3]["type"] == "action"
    assert starts[3]["subtype"] == "element"
    assert starts[3]["command"]["name"] == "multiplication_assignment"

glyph_with_action_list_strand = """
╰──╮╰─╮╰─╮
   │ ─┘  │
     ────┘
      ╭
      │
      │
      ╰─
"""
glyph_with_action_list_strand = [list(ln) for ln in glyph_with_action_list_strand.splitlines()] # format
glyph_with_action_list_strand = glyph_with_action_list_strand[1:] # remove first line

def test_identify_action_list_strand():
    "Test a glyph with an action list strand"
    intr = Lexer()
    gl = [{"glyph": copy.deepcopy(glyph_with_action_list_strand)}]
    intr._load_primes(gl)
    starts = intr.lex_glyph(gl[0]["glyph"])
    assert len(starts) == 4
    assert starts[3]["type"] == "action"
    assert starts[3]["subtype"] == "list"
    assert starts[3]["command"]["name"] == "multiplication_assignment"

glyph_with_action_horz_l2l_strand = """
╰──╮╰─╮╰─╮
   │ ─┘  │
     ────┘
      ╭
      │
      │
      ╰─╶
"""
glyph_with_action_horz_l2l_strand = [list(ln) for ln in glyph_with_action_horz_l2l_strand.splitlines()] # format
glyph_with_action_horz_l2l_strand = glyph_with_action_horz_l2l_strand[1:] # remove first line

def test_identify_action_horz_l2l_strand():
    "Test a glyph with an action list strand"
    intr = Lexer()
    gl = [{"glyph": copy.deepcopy(glyph_with_action_horz_l2l_strand)}]
    intr._load_primes(gl)
    starts = intr.lex_glyph(gl[0]["glyph"])
    assert len(starts) == 4
    assert starts[3]["type"] == "action"
    assert starts[3]["subtype"] == "list2list"
    assert starts[3]["command"]["name"] == "multiplication_assignment"

# question strand set
glyph_with_question_strands = """
╰──╮╰─╮╰─╮╷
   │ ─┘  ││
╭───╮╶───┘│
╰─╮ │ ╭───┘
╭─╯ │ │╭──╮
╰─╮ │ ╷│╭─╯
╭─┘ ╰─┘│╰─╮
╰──────╯ ─╯
"""
glyph_with_question_strands = [list(ln) for ln in glyph_with_question_strands.splitlines()] # format
glyph_with_question_strands = glyph_with_question_strands[1:] # remove first line

def test_correct_count_ends_with_left_facing():
    "Find the correct starts for a glyph with a question strand set where a questions strand ends facing left"
    intr = Lexer()
    gl = [{"glyph": copy.deepcopy(glyph_with_question_strands)}]
    intr._load_primes(gl)
    starts = intr._find_strand_starts(gl[0]["glyph"])
    assert len(starts) == 5

def test_identify_question_strands():
    "Test a glyph with a question strand set"
    intr = Lexer()
    gl = [{"glyph": copy.deepcopy(glyph_with_question_strands)}]
    intr._load_primes(gl)
    starts = intr.lex_glyph(gl[0]["glyph"])
    assert starts[3]["type"] == "question_marker"
    assert starts[3]['x'] == 10
    assert starts[3]['y'] == 0
    assert starts[3]['end_x'] == 6
    assert starts[3]['end_y'] == 5
    assert starts[4]["type"] == "question_marker"
    assert starts[4]['x'] == 6
    assert starts[4]['y'] == 5
    assert starts[4]['end_x'] == 9
    assert starts[4]['end_y'] == 7
