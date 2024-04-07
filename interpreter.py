from argparse import ArgumentParser
from functools import reduce
from operator import itemgetter
import math
import os
import re
from _lexicon import LETTERS


def _chars_in_str(list1, str2):
    retset = []
    for val in list1:
        retset += [m.start() for m in re.finditer(val, str2)]
    return retset
    # return reduce(lambda v1,v2: v1 or v2, map(lambda v: v in list2, list1))


class interpreter:

    def calculate(self, glyph, y, x, dir, val):
        pass

    def get_symbol_by_name(self, name:str):
        retlist = []

        for ltr in LETTERS:
            if ltr["name"] == name:
                retlist += ltr["symbol"]

        return retlist
    
    # def starting_places(self, glyph):
    #     # find starting place for each strand
    #     starts = []

    #     for num, ln in enumerate(glyph):
    #         for i, letter in enumerate(ln): 
    #             if letter in interpreter.LETTERS["int_start"]["right"] and (num == 0 or glyph[num-1][i] not in interpreter.LETTERS["up_cont"]):
    #                 starts.append({"y": num, "x": i, "dir": "right"})
    #             if letter in interpreter.LETTERS["int_start"]["left"] and (num == 0 or glyph[num-1][i] not in interpreter.LETTERS["up_cont"]):
    #                 starts.append({"y": num, "x": i, "dir": "left"})
    #             if letter in interpreter.LETTERS["int_start"]["down"] and (i == 0 or ln[i-1] not in interpreter.LETTERS["left_cont"]):
    #                 starts.append({"y": num, "x": i, "dir": "down"})
    #     return starts

    def _find_strand_starts(self, glyph):
        pass

    def _shave_glyph(self, glyph):
        "Remove starts and ends from a glyph and determine block level"
        level = 1

        while 0 in _chars_in_str(self.get_symbol_by_name("start_glyph"),glyph[0]) and all(y[0] == ' ' for y in glyph):
            level += 1
            glyph = [ln[1:] for ln in glyph]
        glyph[0, 0] = ' '

        if glyph[len(glyph)-1,len(len(glyph-1))-1] == self.get_symbol_by_name("end_glyph"):
            glyph[len(glyph)-1,len(len(glyph-1))-1] = ' '
        else:
            raise Exception("Could not find end glyph")

        return [glyph, level]

    def interpret_glyph(self, glyph):
        starts = self._find_strand_starts(glyph)
        print(starts)

    def _locate_glyphs(self, program):
        """find all the starts and ends where:
            - everything to the left of start up to row of end is blank
            - everything to the bottom of end back to start is blank
        """
        glyph_locs = [] # return set

        starts = []
        ends = []
        
        for y, ln in enumerate(program):
            for x in _chars_in_str(self.get_symbol_by_name("start_glyph"), ln):
                starts.append({"y":y, "x":x})
            for x in _chars_in_str(self.get_symbol_by_name("end_glyph"), ln):
                ends.append({"y":y, "x":x})
        
        for s in starts:
            for e in ends:
                # blank to the left, blank below

                if e["x"] <= s["x"] or e["y"] <= s["y"]:
                    continue

                if (s["x"] == 0 \
                    or all(c == ' ' for c in program[s["y"]-1:s["y"]])) and \
                    (s["x"] == len(program)+1 or \
                    all(c == ' ' for c in program[e["y"]+1][s["x"]:e["x"]+1])):
                    
                    glyph_locs.append({"start":s,"end":e})

        # some kind of check here: overlaps? re-used ends?
                            
        return glyph_locs
    
    def interpret_program(self, program):
        # turn into a grid
        program = program.splitlines()

        glyph_locs = self._locate_glyphs(program)

        glyphs = [] # each glyph as its own matrix
        for g in glyph_locs:
            glyphs.append([row[g["start"]["x"]:g["end"]["x"]+1] for row in program[g["start"]["y"]:g["end"]["y"]+1]])

        block_tree = []
        for glyph in glyphs:
            level, glyph = self._shave_glyph(glyph)
            block_tree.append({"level":level, "glyph":glyph})
        
        for block in block_tree:
            self.interpret_glyph(block["glyph"], block["level"])


    def interpret_file(self, progfile, outfile, verbose):
        self.outfile = outfile
        self.verbose = verbose

        with open(progfile, "r", encoding="utf-8") as file:
            self.interpret_program(file.read())


interpreter.PRIMES_TO_COUNT = 100 # assume a glyph will not be taller than this
# FIXME: we ought to count the size of glyphs on file input and then determine the size used

interpreter.primes = [1]
for num in range(2, interpreter.PRIMES_TO_COUNT ^ 2):
    if all(num%i!=0 for i in range(2,int(math.sqrt(num))+1)):
        interpreter.primes.append(num)
        if len(interpreter.primes) > interpreter.PRIMES_TO_COUNT:
            break


if __name__ == "__main__":

    parser = ArgumentParser(description='Rivulet Interpreter 0.1', 
                            epilog='More at https://danieltemkin.com/Esolangs/Rivulet')

    parser.add_argument('progfile', metavar='progfile', type=str, 
                        help='Rivulet program file')
    parser.add_argument('--out', dest='outfile', default=None, 
                        help='where to write output from the program')
    parser.add_argument('-v', dest='verbose', action='store_true', 
                        default=False, help='verbose logging')
    args = parser.parse_args()

    intr = interpreter()
    result = intr.interpret_file(args.progfile, args.outfile, args.verbose)

    if not args.outfile or args.verbose:
        print(result)