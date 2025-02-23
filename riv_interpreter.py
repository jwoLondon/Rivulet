"Interpreter for the Rivulet esolang"
from argparse import ArgumentParser
from riv_parser import Parser
from riv_python_transpiler import PythonTranspiler
from riv_svg_generator import SvgGenerator

VERSION = "0.1"

class Interpreter:
    "Interpreter for the Rivulet esolang"

    def __init__(self):
        self.outfile = None
        self.verbose = False

    def interpret_file(self, progfile, outfile, verbose, svg):
        "Interpret a Rivulet program file"
        self.outfile = outfile
        self.verbose = verbose

        with open(progfile, "r", encoding="utf-8") as file:
            program = file.read()

        parser = Parser()

        parse_tree = parser.parse_program(program)

        if svg is not None:
            svg = SvgGenerator()
            svg.generate(parse_tree)

        return self.__interpret(parse_tree)
    
    def interpret_program(self, program, verbose):
        "Interpret a Rivulet program passed by text"
        self.verbose = verbose

        parser = Parser()

        parse_tree = parser.parse_program(program)

        return self.__interpret(parse_tree)
    
    def __interpret(self, parse_tree):
        # For now, we print to verify the parse tree
        printer = PythonTranspiler()
        printer.print_program(parse_tree, pseudo=True)


if __name__ == "__main__":

    arg_parser = ArgumentParser(description=f'Rivulet Interpreter {VERSION}',
                            epilog='More at https://danieltemkin.com/Esolangs/Rivulet')

    arg_parser.add_argument('progfile', metavar='progfile', type=str,
                        help='Rivulet program file')
    arg_parser.add_argument('--out', dest='outfile', default=None,
                        help='where to write output from the program')
    arg_parser.add_argument('-v', dest='verbose', action='store_true',
                        default=False, help='verbose logging')
    arg_parser.add_argument('--svg', dest='svg', default=None,
                        help='save to svg')
    args = arg_parser.parse_args()

    intr = Interpreter()
    result = intr.interpret_file(args.progfile, args.outfile, args.verbose, args.svg)

    if not args.outfile or args.verbose:
        print(result)
