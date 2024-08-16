from argparse import ArgumentParser
from functools import reduce
import jmespath
import json
import math


def _chars_in_list(list1, list2):
    retset = []
    for val in list1:
        retset += [i for i in range(len(list2)) if list2[i] == val]
    return retset

OPPOSITE_DIR = {
    "up": "down",
    "down": "up",
    "right": "left",
    "left": "right"
}

class Interpreter:

    def __init__(self):
        with open('_lexicon.json') as lex:
            self.lexicon = json.load(lex)

    def calculate(self, glyph, y, x, dir, val):
        pass

    def get_symbol_by_name(self, name:str):
        retlist = []

        for ltr in self.lexicon:
            if ltr["name"] == name:
                retlist += ltr["symbol"]

        return retlist
    

    def _get_neighbor(self, x, y, dir, glyph, include_coords=False):
        if dir == "up" and y > 0:
            if include_coords:
                return {"symbol": glyph[y-1][x], "x": x, "y": y-1}
            return glyph[y-1][x]
        elif dir == "left" and x > 0:
            if include_coords:
                return {"symbol": glyph[y][x-1], "x": x-1, "y": y}
            return glyph[y][x-1]
        elif dir == "down" and y < len(glyph)-1:
            if include_coords:
                return {"symbol": glyph[y+1][x], "x": x, "y": y+1}
            return glyph[y+1][x]
        elif dir == "right" and x < len(glyph[y])-1:
            # this assumes the glyph is a perfect rect
            if include_coords:
                return {"symbol": glyph[y][x+1], "x": x+1, "y": y}
            return glyph[y][x+1]

    def _check_is_start(self, x, y, glyph):

        symbol = jmespath.search(f"[?symbol.contains(@,`{glyph[y][x]}`)]", self.lexicon)

        # symbol has no reading, ignore
        if not symbol or len(symbol) == 0:
            return
        
        readings = jmespath.search("[].readings[]", symbol)

        # symbol has no starts, ignore
        if not any(r["pos"] == "start" for r in readings):
            return

        # check that it has one but not both sides of a corner or a continue
        successful_matches = []

        # assuming only one reading of this kind
        cont = [r for r in readings if r["pos"] == "corner" or r["pos"] == "continue"]

        if not cont:
            raise Exception(f"Internal Error: No corner or continue in start for {symbol[0]}")

        for dir in cont[0]["dir"]:
            nbr = self._get_neighbor(x, y, dir, glyph)
            if not nbr:
                continue
            nbr_reads = jmespath.search(f"[?symbol.contains(@,`{nbr}`)].readings[]", self.lexicon) 
            if not nbr_reads:
                continue
            nbr_c_reads = [n for n in nbr_reads if n["pos"] == "corner" or n["pos"] == "continue"] #FIXME: Can this be done through jmespath so we don't do this twice?
            if not nbr_c_reads:
                continue

            if OPPOSITE_DIR[dir] in nbr_c_reads[0]["dir"]:
                successful_matches.append(dir)

        if len(successful_matches) != 1:
            return
        
        start_w_dir = [r for r in readings if r["pos"] == "start" and r["dir"] == successful_matches[0]]

        if len(start_w_dir) != 1:
            raise Exception(f"Internal Error: {len(start_w_dir)} dirs in a start where 1 was expected")
        
        return {
            "symbol": symbol[0]["symbol"],
            "name": symbol[0]["name"],
            "x": x,
            "y": y,
            "dir": successful_matches[0],
            "pos": "start",
            "type": start_w_dir[0]["type"]
        }


    def _find_strand_starts(self, glyph):
        starts = []
        for y in range(0, len(glyph)):
            for x in range(0, len(glyph[y])):
                token = self._check_is_start(x, y, glyph)
                if token:
                    starts.append(token)
        return starts


    def _shave_glyph(self, glyph):
        "Remove starts and ends from a glyph and determine block level"
        level = 1

        while 0 in _chars_in_list(self.get_symbol_by_name("start_glyph"),glyph[0]) and all(y[0] == ' ' for y in glyph[1:]):
            level += 1
            glyph = [ln[1:] for ln in glyph]
        glyph[0][0] = ' '

        # replace last glyph in array with a blank if it is an end_glyph
        if glyph[-1][-1] in self.get_symbol_by_name("end_glyph"):
            glyph[-1][-1] = ' '
        else:
            raise Exception("Could not find end glyph")

        return [glyph, level]



    def _interpret_strand(self, glyph, prev, start):
        """Recursively follow the data strand to determine if it is a value or ref strand and build out its value. Parameters:
            glyph: the glyph matrix
            prev: the current step's data (it will advance to the next step)
            start: the start of the strand
        This will modify the start object in place.
        """
        # At the beginning of a strand, prev is the hook which begins it (and never has any other reading).
        # We already know the direction prev is pointing, so we can look for the next character in that direction and mark as curr.
        curr = self._get_neighbor(prev["x"], prev["y"], prev["dir"], glyph, include_coords=True)

        # next_dir is the direction AFTER curr
        next_dir = False

        # symbol is the lexicon entry for curr's character
        symbol = jmespath.search(f"[?symbol.contains(@,`{curr['symbol']}`)]", self.lexicon)

        if not symbol or len(symbol) == 0:
            if (curr['symbol'] == ' '):
                raise Exception(f"Internal Error: Blank space found at {curr['x']},{curr['y']}")
            raise Exception(f"Internal Error: No symbol found for {curr['symbol']}")
        if len(symbol) > 1:
            raise Exception(f"Internal Error: More than one symbol found for {curr['symbol']}")

        readings = {}
        for r in jmespath.search("[].readings[]", symbol):
            readings[r["pos"]] = r

        if "continue" in readings or "corner" in readings:
            # if it's for the matching direction
            if OPPOSITE_DIR[prev['dir']] in r['dir']:
                # remove entries from r['dir'] matching opposite of start['dir']
                next_dir = set(r['dir']) - set([OPPOSITE_DIR[prev['dir']]])
                if len(next_dir) != 1:
                    raise Exception("Internal Error: More than one direction in next step")
                next_dir = next_dir.pop()

        # if it is moving left/right with a continue, add to value
        if "continue" in readings and next_dir:

            if not "value" in start:
                start["value"] = 0

            # if it's straight and left or right, we add or subtract the prime
            if next_dir == 'right':
                start['value'] += self.primes[curr["y"]]
            elif next_dir == 'left':
                start['value'] -= self.primes[curr["y"]]

        # test for end
        if "end" in readings or "loc_marker" in readings:
            if next_dir:
                # check if the strand ends here
                following = self._get_neighbor(curr['x'], curr['y'], next_dir, glyph)
                following = jmespath.search(f"[?symbol.contains(@,`{following}`)]", self.lexicon)

            # if it's possible this is also a continue, we need to check if the next step is in the opposite direction, to rule out a "continuing" reading of the same symbol
            # NOTE: We can't end on a corner or it would be a "hook" to start a strand
            if next_dir:
                opposite_dir_readings = len(jmespath.search(f"[].readings[].dir[?contains(@,'{OPPOSITE_DIR[next_dir]}')][]", following))
            if not next_dir or not following or not ("continue" in readings and opposite_dir_readings > 0, following):
                # if it's a value strand, we need to mark it as such
                # check if the loc_marker reading has the right direction
                if "loc_marker" in readings and OPPOSITE_DIR[prev['dir']] in readings["loc_marker"]['dir']:
                    start['value'] = None
                    start['type'] = "ref"
                    start['end_x'] = curr['x']
                    start['end_y'] = curr['y']
                else:
                    # mark the ref strand
                    start['type'] = "value"

                return
            
        # if it continues, load the next character
        if ("continue" in readings or "corner" in readings) and next_dir:
            curr["dir"] = next_dir
            self._interpret_strand(glyph, curr, start)
            return
        
        raise Exception(f"Internal Error: No valid reading found for char at {curr['x']},{curr['y']}")


    def lex_glyph(self, glyph, level):
        starts = self._find_strand_starts(glyph)
        for s in starts:
            if s['type'] == 'data':
                # we don't know yet if it is a value strand or ref strand
                # print(s['dir']) # 'left', 'right', 'up', 'down'
                self._interpret_strand(glyph, s, s)
        return starts


    def _locate_glyphs(self, program):
        """find all the starts and ends where:
            - everything to the left of start up to row of end is blank
            - everything to the bottom of end back to start is blank
        """
        glyph_locs = [] # return set

        starts = []
        ends = []
        
        for y, ln in enumerate(program):
            for x in _chars_in_list(self.get_symbol_by_name("start_glyph"), ln):
                # make sure immediate left does not also have start symbol
                # FIXME: this should also determine the glyph's level
                if not ln[x-1] in self.get_symbol_by_name("start_glyph"):
                    starts.append({"y":y, "x":x})
            for x in _chars_in_list(self.get_symbol_by_name("end_glyph"), ln):
                ends.append({"y":y, "x":x})
        
        for s in starts:
            for e in ends:

                if e["x"] <= s["x"] or e["y"] <= s["y"]:
                    continue

                # blank or beg of file above and not any horiz break in the middle
                if (s["y"] == 0 or all(c == ' ' for c in program[s["y"]-1])) and \
                    not any(all(c == ' ' for c in program[y]) for y in range(s["y"],e["y"])):

                    # no col to the right or all blanks to the right and no vert break in the middle
                    if (e["x"] == len(program)-1) or \
                        (all(c == ' ' for c in [arr[e["x"]+1] if len(arr) > e["x"]+1 else ' ' for arr in program[s["y"]:e["y"]]])) and \
                        not any(all(c == ' ' for c in [arr[x] if len(arr) > x else ' ' for arr in program[s["y"]:e["y"]]]) for x in range(s["x"],e["x"])):

                        glyph_locs.append({"start":s,"end":e})

        return glyph_locs
    
    def _load_primes(self, glyphs):
        self.primes = [1]
        primes_to_count = max([len(i) for i in glyphs])
        for num in range(2, primes_to_count ** 2):
            if all(num%i!=0 for i in range(2,int(math.sqrt(num))+1)):
                self.primes.append(num)
                if len(self.primes) >= primes_to_count:
                    break
    
    def interpret_program(self, program):
        # turn into a grid
        program = [list(ln) for ln in program.splitlines()]

        glyph_locs = self._locate_glyphs(program)

        glyphs = [] # each glyph as its own matrix
        for g in glyph_locs:
            glyphs.append([row[g["start"]["x"]:g["end"]["x"]+1] for row in program[g["start"]["y"]:g["end"]["y"]+1]])

        block_tree = []
        for glyph in glyphs:
            level, glyph = self._shave_glyph(glyph)
            block_tree.append({"level":level, "glyph":glyph})

        # now that we know the # of lines of the longest glyph, we calculate the primes for the whole list
        self._load_primes(glyphs)
        
        self.glyphs = []
        for block in block_tree:
            self.glyphs.append(self.lex_glyph(block["level"], block["glyph"]))

        # debug
        print(self.glyphs)



    def interpret_file(self, progfile, outfile, verbose):
        self.outfile = outfile
        self.verbose = verbose

        with open(progfile, "r", encoding="utf-8") as file:
            program = file.read()

        self.interpret_program(program)


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

    intr = Interpreter()
    result = intr.interpret_file(args.progfile, args.outfile, args.verbose)

    if not args.outfile or args.verbose:
        print(result)