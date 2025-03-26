![Python versions](https://img.shields.io/badge/Python-3.12-blue)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

# Rivulet

Rivulet is a programming language of flowing strands, written in semigraphic characters. A strand is not pictographic: its flow does not simulate computation. There are four kinds of strands, each with their own symbolism and grammatical rules. Together, they form glyphs, tightly-packed blocks of code whose strands execute together.

Here is a complete Fibonacci program:
```
   ╵──╮───╮╭─    ╵╵╭────────╮
    ╰─╯╰──╯│       ╰─╶ ╶╮╶╮╶╯
   ╰─────╮ │      ╭─────╯ ╰─────╮
         ╰─╯ ╷    ╰───       ───╯╷

   ╵╵─╮  ╭─╮     ╭──       ╵╵╰─╮  ──╮──╮
      ╰─╮│ ╰─╯ ╵╵╰─╯╶╮       ╴─╯  ╭─╯╭─╯
      ╰─╯╰─ ╰──╯╰────╯       ╭╴ ╵╶╯ ╶╯╶╮
        ╭─╮ ╭╴               │  ╰──────╯
        │ │ │                ╰─╮       ╭─╮ 
      │ │ ╰─╯                  │     │   │
      ╰─╯            ╷         ╰──── ╰───╯╷

   ╵╵ ╭──  ──╮  ╭─╮         ╵╰─╮
      ╰─╮  ╭─╯╭─╯ │          ╴─╯
       ╶╯╵╶╯  │ ╷╶╯          ╭─╮
     ╭─╮ ╰────╯ │   ╭─╮        │
     │ ╰────╮ ╭─╯ ╭╴│ │      ╭─╯
     ╰────╮ │ │ │ │ │ │      │
     ╭────╯ │ │ ╰─╯ │ ╷      ╰─╷
     ╰────╮ │ ╰─────╯ │  
          │ ╰─────────╯╷
```

Here is the same program formatted by the interpreter into an svg, alongside two variations that produce equivalent computer instructions: 

<img src="images/fibonacci1.png" width=32% height=32%>
<img src="images/fibonacci2.png" width=32% height=32%>
<img src="images/fibonacci4.png" width=32% height=32%>

| :warning: WARNING          |
|:---------------------------|
| **Status: Version 0.4**. This is a mostly-working interpreter, and a tool to generate svg files of source code. The command list will likely need to expand for usability. |

## Design Philosophy

Rivulet is a list-based language that avoids ordinary approaches to branching and looping. Strands never split and no strand is left un-executed.

Its writing system was inspired by the satisfying compactness of mazes, Anni Albers's Meanders series, and space-filling algorithms. Its calligraphic aspects draw from natural language and favor the ability to write by hand.

## Data Model

In Rivulet, data is organized into lists of adjacent cells, populated with zeros by default. Commands are applied to either a single cell or an entire list. They take a second parameter, a constant or the value of another cell. 

Commands can also be run list-to-list, applying the command to each successive cell of one list, from the corresponding cells of the other. While these consider zero-populated cells as well, a list-to-list command ends at the last cell holding a value in either list.

The first list, List 1, is sometimes used as the output stream. This is an interpreter setting, as is whether they are displayed as numerical data or a Unicode string (where each value is rounded to the nearest integer).

## Control Flow

Every strand of every glyph runs in a Rivulet program; there is no equivalent of an "if" statement. If a glyph leads to an unwanted state, that glyph and the others of its block (all contiguous glyphs of the same level or higher), can be rolled back, setting the execution state to what it was before the glyph (or set of glyphs) fired. The conditional rollback is the only form of branching in Rivulet. Loops only end with a rollback of their last iteration. Tests for rollback are that a single cell or an entire list is either zero or non-zero, indicated by a special strand called the Question Strand.

Data strands are run in the order they begin at the top left, moving through each column flowing to the right. So the strand beginning at coordinate 2,0 is run, then 2,1, then 3,0, and so on. Question strands are always run after the data strands are executed.

## Syntax

Rivulet's nuanced grammar may seem overwhelming at first but becomes easy to read and write with practice.

### Glyphs

Glyphs begin with markers: ╵ in the upper left and end with ╷ at the bottom right. They must not have a vertically-oriented character directly above or below them, or they'll be confused for strands. Any text outside of glyph markers is ignored.

The level of the glyph is marked by how many ╵s appear at the beginning of the glyph. Levels tell where glyphs fall within larger blocks of code.

Glyphs can be arranged vertically or side-by-side. They are read in the order of their starting marker location: top-to-bottom, left-to-right.

In other words, this program:

    1 ╵╰──╮╰─ ╭──╯ ╶╮
    2    ─┘   └─    │
    3    ╭──────────┘
    5    └────────  ╷

    1 ╵╵     ╭───╮ ╭─
    2    ╴─╮╶╯╶╮ ╷╶╯
    3  ╵╰──┘   │
    5  ╰───────╯

is identical to this one:

    1 ╵╰──╮╰─ ╭──╯ ╶╮ ╵╵     ╭───╮ ╭─
    2    ─┘   └─    │    ╴─╮╶╯╶╮ ╷╶╯
    3    ╭──────────┘  ╵╰──┘   │
    5    └────────  ╷  ╰───────╯


### Lines of code

The interpreter refers to code locations in terms of glyph numbers and then line numbers. Line numbers reset to 1 in each glyph. After line 1, they are numbered for each successive prime. These numbers are semantically meaningful for some strands.

Other strand types use horizontal line numbers, counting in primes away from their starting hook. They always begin on line 1 and their neighbors are 2 on each side. They progress through primes, but always in distance from their starting point. Line numbers are every-other-line vertically: this is so vertical lines are not packed too tightly.

Here are examples of such strands:

      ╭─╮ ╭╴  ╭╴ 
      │ │ │   │ │
    │ │ ╰─╯   │ │
    ╰─╯       ╰─╯
	5 3 2 1   1 2

## Lexemes

Rivulet commands are written with these signs. Some re-use characters in a way that only context can disambiguate:

| Name      | Signs | Context | Interpretation
| --- | --- | --- | --- |
| Glyph Start and End | ╵ ╷ | Not be adjacent another sign with a vertical reading | Marks the glyph, the smallest block of code in Rivulet 
| Location | ╵ ╷ ╴╶ | Leaves a gap, to punctuate the end of a strand e.g. from left: ──╶ | A reference pointer to a cell
| Continue | ─ │ | Continues the flows in the same direction e.g.  ──── | Depending on the strand type, it can add or subtract the line number of its horizontal or vertical line number, or simply continue the strand
| Corner |╯┘╰└ ╮┐╭┌ | Sharp or curved corners have the same meaning and can be used interchangeably | Turns direction of flow
| Hook | ╯┘╰╴└╴ ╮┐╭╴┌╴| It's a character or characters that turn ninety degrees at the beginning of some strands. If it turns to the right or left, it is extended with a half-length line, the same character used to indicate Location, but flipped to extend the hook and not leave a gap.
| Non-hook Begin Strand | ╷ above a │| Strands with no hook begin with the half-length character to extend it | Marks the beginning of a Question Strand


## Data Strands

### Value Strands

A value strand indicates a command that takes a constant value. Value strands (and other data strands), begin with a hook that points up (as in the third strand below) or to the left (as in the first two). All three of the strands below are value strands:

    1 ╵╰──╮╭──╯╶╮
    2    ─┘└─   └─╮
    3               
    5              ╷

Each of these value strands writes to list 1, as their hooks sit on line 1. The first strand writes to the first cell (cell 0), as it appears first on that line, the second writes to the second cell (cell 1), etc.

The first strand moves two spaces (two ── characters) to the right on line 1, adding 1 twice. It then moves one ── to the left on line 2, subtracting two. This leaves zero. This makes the first strand a *zero strand*. The default command applied to a strand is addition assignement, and so zero strands usually invoke no operation.

The second strand is also a zero strand: it makes the same motions in reverse of the first strand, subtracting two and then adding two strand back.

The third strand adds the value two to the third cell or list 1. The importance of the two zero strands is in marking the third strand to write to cell 2 of list 1, rather than cell 0.

### Reference Strands

Reference strands look identical to value strands, only they end with a Location Marker, a small gap that punctuates the end of the strand. It appears in the two top strands here:

    1 ╵╰──╮  ╭──╯
    2   ╴─┘╶╮└─╶ 
    3       └─╮        
    5            ╷

The movement of Reference Strands back and forth through the glyph has no effect on what they reference; only where they end.

The first strand above is no longer a Zero Strand, but a reference to the first cell (cell 0) of List 2. The second strand beginning on line 1 refers to the second cell (cell 1) of List 2. This is because between those two strands is a strand writing to cell 0 of List 2. If we wanted both of the top strands to read from cell 0 of List 2, we would move its end to before that assignment (here using the vertical version of the Location Marker):

    1 ╵╰──╮╭────╯
    2   ╴─┘╷╶╮ 
    3        └─╮        
    5            ╷

## Action Strands

The default command is addition assignment ( += ). To choose another commands, we create an Action Strand to apply to an existing data strand.

Action Strands have hooks that point down or to the right. They sit directly below the data strand they apply to. If two data strands' hooks are aligned vertically, the top action strand applies to the top data strand, the second to the second, etc.

Where a data strand's value is determined by movements to the left and right, action strands determine value through vertical movement. Their line numbers are independent of the other strands in the glyph, each beginning with line 1 as the column where they begin. Their neighbors to the left and right are line 2, followed by 3 and 5. 

EXAMPLE: This command that raises the values of list 1, cells 0 and 1, each to their fourth power:

     1 ╵╰─╮ ╰─╮
     2    │   │ 
     3  ╭╴└─╭╴└─
     5  │   │ 
	 7  │   │
    11  ╰─╮ ╰─╮
    13    │   │ ╷
        1 2 1 2

The action strands each have a value of 4, which corresponds to exponentiation_assignment, under data strands of value 4. Here is the (INCOMPLETE) command list, showing which values assign to what command:

| Value  | Command | Interpretation |
| --- | --- | --- |
| default | addition_assignment | add to location, set to zero by default |
| 0 | overwrite | assignment, overwriting existing value |
| 1 | insert | inserts value after indicated cell |
| -1 | subtraction assignment | |
| 2 | multiplication assignment | |
| -2 | division assignment | |
| 3 | no-op | TBD; currently only has value when assigned to list |
| -3 | mod assignment | modulus of cell value against supplied argument |
| 4 | exponentiation assignment | raise to power of supplied argument" |
| -4 | root assignment | take root at power of supplied argument |


:WARNING: It is every-other-line that increments between the primes, as the vertical length for a block-drawing char is longer than their horizontal length. This sounds confusing but is usually clear visually.

Here is an example of two action strands and their numbering:

      ╭─╮ ╭╴  ╭╴ 
      │ │ │   │ │
    │ │ ╰─╯   │ │
    ╰─╯       ╰─╯
    5 3 2 1   1 2

The first strand has a value of: (1 - 2 + 2*3 - 5) = 2, multiplication assignment. The second strand has a value of (2 * 1) - (2 * 2) = -2, division assignment.

### List indicator

Action strands can also mark that a command applies not to a single cell (as is the default) but to an entire list. This is indicated by ending an action strand with a horizontal movement. When a list indicator appears, the data strand maintains the same order as if it were its cell that updates. If cell 3 has an action strand, it is still run after cell 2 and before cell 4 strands.

### List 2 List

If an action strand ends with a location marker (the tiny gap), it shows that the action should be applied for every cell of the referenced list to every cell of the assigned list. This is only syntactically valid when the data strand also ends with a location marker (is a reference strand).

Every cell with a number in the second list is applied to the cells in the first.

## Question Strand Sets

Question Strands appear in pairs, one above the other.

Together, they pose a question about the state of the data. Should it be found wanting, the glyph and its siblings (those at the same level) are rolled back. If in a loop, only the most recent iteration is undone. This is the only way to exit a loop.

The top question strand begins with a vertical line. It ends either to the left or right of where it began (above or below has no semantic meaning).

The bottom question strand begins directly above its partner. It too ends either to the left or right of where it began, and it ends with a vertical piece (indicating the question applies only to a single cell) or a horizontal piece (indicating the entire list is to be questioned, the answer an accumulation of its answer).

Question strands, read only by their beginning vs end, can move back and forth through the glyph, filling in blank spaces. They are often decorative, gap-filling lines.

Question lines always fail if an item is less than or equal to zero.

| Top Line | Bottom Line | Use | Checks
| --- | --- | --- | --- |
| Left | Horizontal | If | List (all items)
| Left | Vertical | If | Cell
| Right | Horizontal | While | List
| Right | Vertical | While | Cell

(any) vs (all) are equivalent if testing only a single cell
