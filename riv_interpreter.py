"Interpreter for the Rivulet esolang"
from argparse import ArgumentParser
from riv_parser import Parser

VERSION = "0.1"

class Interpreter:
    "Interpreter for the Rivulet esolang"

    def __init__(self):
        self.outfile = None
        self.verbose = False

    def interpret_file(self, progfile, outfile, verbose):
        "Interpret a Rivulet program file"
        self.outfile = outfile
        self.verbose = verbose

        with open(progfile, "r", encoding="utf-8") as file:
            program = file.read()

        parser = Parser()

        parser.parse_program(program)

        return ""


if __name__ == "__main__":

    arg_parser = ArgumentParser(description=f'Rivulet Interpreter {VERSION}', 
                            epilog='More at https://danieltemkin.com/Esolangs/Rivulet')

    arg_parser.add_argument('progfile', metavar='progfile', type=str, 
                        help='Rivulet program file')
    arg_parser.add_argument('--out', dest='outfile', default=None, 
                        help='where to write output from the program')
    arg_parser.add_argument('-v', dest='verbose', action='store_true', 
                        default=False, help='verbose logging')
    args = arg_parser.parse_args()

    intr = Interpreter()
    result = intr.interpret_file(args.progfile, args.outfile, args.verbose)

    if not args.outfile or args.verbose:
        print(result)
