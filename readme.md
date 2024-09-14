# Rivulet

Rivulet is a programming language of flowing strands, written in semigraphic characters. A strand is not pictographic: its flow does not simulate computation, its movements are merely symbolic. There are four kinds of strands, each with their own grammatical rules and interpretation. Together, they form glyphs, blocks of code that execute together.

[!WARNING] Status: The Rivulet parser mostly works and can spit out pseudo-code. Question strands are not ready.

## Data Model

In Rivulet, data is organized into lists of adjacent cells, filled with zeros by default. Commands are applied to either a single cell or an entire list. They take a second parameter, a constant or the value of another cell. 

Commands can also be run list-to-list, applying the command to each successive cell, using the corresponding cells of the other. While they apply to cells with zeros as well, it does not go further then the last cell holding a value in either list.

The first list, List 1, is sometimes used as the output stream. This is an interpreter setting, and can be written as numerical data or a Unicode string, with each value rounded to the nearest integer.

## Control Flow

Every Strand of every Glyph runs in a Rivulet program. If a glyph leads to an unwanted state, that glyph and the others of its block (all contiguous glyphs of the same level or higher), can be rolled back. The conditional rollback is the only form of branching in Rivulet. While loops end with a conditional rollback of their last iteration. Tests for rollbacks are that a single cell or entire list is zero.

## Syntax

### Glyphs

Glyphs begin with ╵ in the upper left and end with ╷ at the bottom right. They must not have a vertically-oriented character directly above or below them, or they'll be confused for strands. Any text outside of glyph markers is ignored.

The level of the glyph is marked by how many ╵s appear at the beginning of the glyph. Levels tell where glyphs fall within larger blocks of code.

### Lines of code

The interpreter refers to code locations in terms of glyph numbers and then line numbers. Line numbers reset to 1 in each glyph. After line 1, they are numbered for each successive prime. These numbers are semantically meaningful for some strands.

Some strand types have a vertical reading of line numbers. In their case, they always begin on line 1 and their neighbors are 2 on each side. They progress through primes, but always in distance from their starting point. Line numbers are every-other-line vertically so that the vertical lines are not packed too tightly.

## Lexemes

Rivulet commands are written with these signs. Some re-use characters in a way that only context can disambiguate:

| Name      | Signs | Context | Interpretation
| --- | --- | --- | --- |
| Glyph Begin and End | ╵ ╷ | Not be adjacent another sign with a vertical reading | Marks the glyph, the smallest block of code in Rivulet 
| Location | ╵ ╷ ╴╶ | Leaves a gap, to punctuate the end of a strand e.g. from left: ──╶ | A reference pointer to a cell
| Continue | ─ │ | Continues the flows in the same direction e.g.  ──── | Depending on the strand type, it can add or subtract the line number of its horizontal or vertical line number
| Corner |╯┘╰└ ╮┐╭┌ | Sharp or curved corners have the same meaning and can be used interchangeably | Turns direction of flow
| Hook | ╯┘╰╴└╴ ╮┐╭╴┌╴| It's a character or characters that turn ninety degrees at the beginning of some strands. If it turns to the right or left, it is extended with a half-length line, the same character used to indicate Location, but flipped to extend the hook and not leave a gap.
| Non-hook Begin Strand | ╷ above a │| Strands with no hook begin with the half-length character to extend it | Marks the beginning of a Question Strand


## Data Strands

### Value Strands

A value strand begins with a hook that points up or two the left.

    1 ╵╰──╮╭──╯╶╮
    2    ─┘└─   └─╮
    3               
    5              ╷

### Reference Strands

## Action Strands

## Question Strands

The top question marker begins 

It has a lot of motion, but most of it does almost nothing.

	top line begins directly under an END of a line:
		applies to that cell

	top line does not:
		applies to the entire list that it starts from, not that it is under

	top line left of where it begins: 



