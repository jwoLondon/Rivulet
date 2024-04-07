from argparse import ArgumentParser
from operator import itemgetter
import math
import os
import re


class interpreter:

    LETTERS = {
        "start_glyph": "╵",
        "end_glyph": "╷",

        # for initial assign or add
        "int_start": {
            "right": ["╰","└"],
            "left": ["╯","┘"],
            "down": ["╮","┐"]
        },
        # for apply to substr (up to two) labeled by assoc prime number
        # or clip away, for those that take no command
        "clip_start": {
            "downright": ["╭","┌"],
            "up": ["╰","└"]
        },
        # for all commands
        "cmd_start": {
            "down": ["╷"],
            "up": ["╯","┘"]
        },
        "up_cont": ["│","╮","┐","╭","┌"], # marks continuation of int_start ups
        "left_cont": ["─","╰","└","╭","┌"], # marks cont of int_start down
        "down_cont": ["│","╰","└","╯","┘"], 
        "right_cont": ["─","╯","┘","╮","┐"]
    }

    def calculate(self, glyph, y, x, dir, val):
        # end with a split with no values for some case?
        # split earlier when we are going to have a test
        # how a split ends determines whether it's a stay / undo / kill parent

        if dir == "down":
            y += 1
        if dir == "up":
            y -= 1
        if dir == "right":
            x += 1
        if dir == "left":
            x -= 1

        if y >= len(glyph):
            return val
        if x >= len(glyph[y]):
            return val

        if (dir == "down" or dir == "up") and glyph[y][x] == "│":
            return self.calculate(glyph, y, x, dir, val)
        if dir == "right" and glyph[y][x] == "─":
            val += interpreter.primes[y]
            return self.calculate(glyph, y, x, dir, val)
        if dir == "left" and glyph[y][x] == "─":
            val -= interpreter.primes[y]
            return self.calculate(glyph, y, x, dir, val)
        if dir == "up" and (glyph[y][x] == "╮" or glyph[y][x] == "┐"):
            return self.calculate(glyph, y, x, "left", val)
        if dir == "right" and (glyph[y][x] == "╮" or glyph[y][x] == "┐"):
            return self.calculate(glyph, y, x, "down", val)
        if dir == "up" and (glyph[y][x] == "╭" or glyph[y][x] == "┌"):
            return self.calculate(glyph, y, x, "right", val)
        if dir == "left" and (glyph[y][x] == "╭" or glyph[y][x] == "┌"):
            return self.calculate(glyph, y, x, "down", val)
        if dir == "down" and (glyph[y][x] == "╯" or glyph[y][x] == "┘"):
            return self.calculate(glyph, y, x, "left", val)
        if dir == "right" and (glyph[y][x] == "╯" or glyph[y][x] == "┘"):
            return self.calculate(glyph, y, x, "up", val)
        if dir == "down" and (glyph[y][x] == "╰" or glyph[y][x] == "└"):
            return self.calculate(glyph, y, x, "right", val)
        if dir == "left" and (glyph[y][x] == "╰" or glyph[y][x] == "└"):
            return self.calculate(glyph, y, x, "up", val)

        return val
    
    def starting_places(self, glyph):
        # find starting place for each constant / command
        starts = []

        for num, ln in enumerate(glyph):
            for i, letter in enumerate(ln): 
                if letter in interpreter.LETTERS["int_start"]["right"] and (num == 0 or glyph[num-1][i] not in interpreter.LETTERS["up_cont"]):
                    starts.append({"y": num, "x": i, "dir": "right"})
                if letter in interpreter.LETTERS["int_start"]["left"] and (num == 0 or glyph[num-1][i] not in interpreter.LETTERS["up_cont"]):
                    starts.append({"y": num, "x": i, "dir": "left"})
                if letter in interpreter.LETTERS["int_start"]["down"] and (i == 0 or ln[i-1] not in interpreter.LETTERS["left_cont"]):
                    starts.append({"y": num, "x": i, "dir": "down"})
        return starts

    def interpret_glyph(self, glyph):
        consts = []
        starts = self.starting_places(glyph)

        for start in sorted(starts, key=itemgetter('x', 'y')):
            for i in range(start["y"] + 1):
                if len(consts) <= i:
                    consts.append([])
            consts[start["y"]].append(self.calculate(glyph, start["y"], start["x"], start["dir"], 0))

        print(consts)

    def interpret_program(self, program):
        glyph_start = -1
        curr_glyph = []

        for ln in program.splitlines():
            if glyph_start < 0 and interpreter.LETTERS["start_glyph"] in ln:
                glyph_start = ln.find(interpreter.LETTERS["start_glyph"])
            if glyph_start > -1:
                curr_glyph.append(ln[glyph_start:])
            if glyph_start > -1 and interpreter.LETTERS["end_glyph"] in ln:
                curr_glyph = [gln[:ln.find(interpreter.LETTERS["end_glyph"]) -  glyph_start] for gln in curr_glyph]

                glyph_start = -1
                self.interpret_glyph(curr_glyph)


    def interpret_file(self, progfile, outfile, verbose):
        self.outfile = outfile
        self.verbose = verbose

        with open(progfile, "r", encoding="utf-8") as file:
            self.interpret_program(file.read())


interpreter.PRIMES_TO_COUNT = 100 # assume a glyph will not be taller than this


interpreter.primes = [1]
for num in range(2, interpreter.PRIMES_TO_COUNT ^ 2):
    if all(num%i!=0 for i in range(2,int(math.sqrt(num))+1)):
        interpreter.primes.append(num)
        if len(interpreter.primes) > interpreter.PRIMES_TO_COUNT:
            break

if __name__ == "__main__":

    parser = ArgumentParser(description='Revert Interpreter 0.1', 
                            epilog='More at https://danieltemkin.com/Esolangs/Revert')

    parser.add_argument('progfile', metavar='progfile', type=str, 
                        help='Revert program file')
    parser.add_argument('--out', dest='outfile', default=None, 
                        help='where to write output from the program')
    parser.add_argument('-v', dest='verbose', action='store_true', 
                        default=False, help='verbose logging')
    args = parser.parse_args()

    intr = interpreter()
    result = intr.interpret_file(args.progfile, args.outfile, args.verbose)

    if not args.outfile or args.verbose:
        print(result)