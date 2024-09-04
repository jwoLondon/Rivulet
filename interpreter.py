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


    def _interpret_strand(self, glyph, prev, start):
        """Recursively follow the data strand to determine build out its value and determine its subtype (value vs ref if data strand etc). Parameters:
            glyph: the glyph matrix
            prev: the current step's data (it will advance to the next step)
            start: the start of the strand
        This will modify the start object in place.
        """
        # At the beginning of a strand, prev is the hook which begins it (and never has any other reading).
        # We already know the direction prev is pointing, so we can look for the next character in that direction and mark as curr.
        curr = self._get_neighbor(prev["x"], prev["y"], prev["dir"], glyph, include_coords=True)

        #TODO: look at start["type"] to determine if data (value or ref), action, or question. currently assumes data

        # next_dir is the direction curr continues onto its following character
        next_dir = False

        # symbol is the metadata, pulled from the lexicon, for curr's character
        symbol = jmespath.search(f"[?symbol.contains(@,`{curr['symbol']}`)]", self.lexicon)

        if not symbol or len(symbol) == 0:
            if (curr['symbol'] == ' '):
                raise Exception(f"Internal Error: Blank space found at {curr['x']},{curr['y']}")
            raise Exception(f"Internal Error: No symbol found for {curr['symbol']}")
        if len(symbol) > 1:
            raise Exception(f"Internal Error: More than one symbol found for {curr['symbol']}")

        # possible interpretations of the character
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

            # if it's possible this is also a continue, we need to check if the next step has a continuation or if this is really the end
            # NOTE: We can't end on a corner or it would be a "hook" to start a strand (no strand can have a hook on both sides)
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
            self._interpret_strand(glyph, s, s)
        return starts

    def _locate_glyphs(self, program):
        """Find all the Starts and Ends where:
            - everything in the col left of Start down to End is blank
            - everything in the row below End back to Start is blank
            - the Start and End are not connected to other symbols
            - the Start and End are not on the same line
          Determine level of glyph
        """
        glyph_locs = [] # return set

        starts = []
        ends = []
        level = 1
        
        for y, ln in enumerate(program):
            for x in _chars_in_list(self.get_symbol_by_name("start_glyph"), ln):
                # make sure immediate right does not also have start symbol
                if x != len(ln) - 1 and not ln[x+1] in self.get_symbol_by_name("start_glyph"):
                    starts.append({"y":y, "x":x})
                    if x > 0 and ln[x-1] in self.get_symbol_by_name("start_glyph"):
                        # find the level of the glyph by walking to the left
                        for i in reversed(range(0, x)):
                            if ln[i] in self.get_symbol_by_name("start_glyph"):
                                level += 1
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
                    if (e["y"] == len(program)-1) or \
                        (all(c == ' ' for c in [arr[e["x"]+1] if len(arr) > e["x"]+1 else ' ' for arr in program[s["y"]:e["y"]]])) and \
                        not any(all(c == ' ' for c in [arr[x] if len(arr) > x else ' ' for arr in program[s["y"]:e["y"]]]) for x in range(s["x"],e["x"])):

                        glyph_locs.append({"start":s,"end":e,"level":level})

        return glyph_locs
    
    def _load_primes(self, glyphs):
        self.primes = [1]
        primes_to_count = max([len(i["glyph"]) for i in glyphs])
        for num in range(2, primes_to_count ** 2):
            if all(num%i!=0 for i in range(2,int(math.sqrt(num))+1)):
                self.primes.append(num)
                if len(self.primes) >= primes_to_count:
                    break

    def _remove_blank_lines(self, program):
        "Clear blank lines from top and bottom of a multi-line string"
        if program[0] == [] or set(program[0]) == {' '}:
            program = program[1:]
        if program[-1] == [] or set(program[-1]) == {' '}:
            program = program[:-1]
        return program
    
    def _prepare_glyphs_for_lexing(self, glyph_locs, program):
        "Returns a set of individual glyphs, each with its level, with the Start and End symbols removed"
        block_tree = []
        for g in glyph_locs:
            # isolate the glyph
            glyph = [row[g["start"]["x"] - g["level"] + 1:g["end"]["x"]+1] for row in program[g["start"]["y"]:g["end"]["y"]+1]]

            # remove the start and end symbols
            for i in range(0, g["level"]):
                glyph[0][i] = ' '
            glyph[-1][-1] = ' '

            block_tree.append({"level":g["level"], "glyph":glyph})

        return block_tree

    
    def interpret_program(self, program):
        # turn into a grid
        program = [list(ln) for ln in program.splitlines()]

        program = self._remove_blank_lines(program)
        glyph_locs = self._locate_glyphs(program)
        glyphs = self._prepare_glyphs_for_lexing(glyph_locs, program)

        # now that we know the # of lines of the longest glyph, we calculate the primes for the whole list
        self._load_primes(glyphs)
        
        for block in glyphs:
            block["tokens"] = self.lex_glyph(block["glyph"])

        # debug
        for glyph in glyphs:
            print(f"tokens: {glyph["tokens"]}")



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