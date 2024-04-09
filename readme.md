
![Python versions](https://img.shields.io/badge/Python-3.12-blue)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

# Rivulet

Rivulet is a language drawn in Unicode block-drawing characters. Each block of code is called a glyph. A glyph is drawn as a maze-like tangle of strands, each of which determines a command. Only the path of these strands are code; there are no keywords drawn from English or other natural languages.

As a glyph completes, the last strand to run is its conditional. If the conditional fails, the glyph undoes itself, rolling the program back to the state before the glyph was executed. In that way, it is the outcome that is tested, rather than the glyph's initial state. Every glyph of every program is executed. There is no way to conditionally run a block of code, only to revert that block after execution.

## Syntax

### Glyphs

Glyphs begin with ╵ and end with ╷

Any large, empty area in the interior of a glyph is a syntax error. Glyphs should be dense.

### Strands

Strands flow. Usually up to down, but not always. They turn using corners;  curved and sharp corners are interchangeable, but generally curved are preferred. There needs to be a certain proportion of sharp corners to add some visual interest. Lack of visual interest is a syntax error.

There are three types of strands, marked by how the strand begins.

#### Values

Values are all assigned as ints. Floats are constructed through division. Ints can be emitted as characters.

#### Command
Most commands are nilads, a few are monads.

#### Conditional Rollback

### Other markers





Blocks of code in Rivulet are called glyphs. A glyph has multiple commands, each represented as a rivulent (or strand). They are drawn with Unicode block drawing characters.

As a strand moves to the left or to the right, the value of that

Indivudal commands are represented as rivulets (or strands) written with Unicode block drawing characters.

Each line of text that a strand moves represents a value. The first line is 1, the rest are ascending prime numbers. Where the line begins marks 

How it moves to the right or left on those lines adds or subtracts from it. The line where a strand begins represents the array it is affecting or being assign to. Each line it crosses represents a constant. The first line is 1, then they progress as ascending prime numbers.

Rivulet is written in glyphs; each glyph is a block of code. Everything in the glyph is executed.

Large gaps in the drawing of a single glyph are syntax errors that cause the glyph to fail.

If there is a conditional in the glyph, it is executed last. A conditional does not branch in the conventional way, like if/then. Instead, the condition tests the outcome of that glyph, and if it fails, it will "undo" the glyph, returning the state of the program back to what it was before the glyph executed.

In that way, conditionals test the outcome of that branch and rollback, rather than 
