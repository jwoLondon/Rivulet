"Tool to create svg files from Rivulet source code"
from enum import Enum
import os
from pathlib import Path
import svg

class SvgGenerator:
    "Tool to create svg files from Rivulet source code"

    # class CellLocHoriz(Enum):
    #     LEFT = 1
    #     MIDDLE = 2
    #     RIGHT = 3
    
    # class CellLocVert(Enum):
    #     TOP = 1
    #     MIDDLE = 2
    #     BOTTOM = 3

    def __init__(self, cell_width=40, cell_height=100):
        self.cell_width = cell_width
        self.cell_height = cell_height

    def generate(self, parse_tree, outfile=False):
        "Generate an SVG file from the parse tree"
        if not outfile:
            outfile = "out/output.svg" # this should increment probly

        d = []

        x_off = 0 # currently assumes vertical layout
        y_off = 0

        for glyph in parse_tree:
            prev_dir = None
            for token in glyph["tokens"]:
                d.append(svg.M((token["x"] + x_off) * self.cell_width, (token["y"] + y_off) * self.cell_height))
                prev_dir = self._process_cell(token, d, prev_dir, True)
                for c in token["cells"]:
                    prev_dir = self._process_cell(c, d, prev_dir, False)
                if token["action"] is not None:
                    prev_dir = self._process_cell(token["action"], d, prev_dir, True)
                    for c in token["action"]["cells"]:
                        prev_dir = self._process_cell(c, d, prev_dir, False)
            y_off += (len(glyph["glyph"]) + 8)

        canvas = svg.SVG(
            width=2000, # TO BE CALCULATED
            height=y_off * self.cell_height,
            elements=[
                svg.Path(
                    d=d,
                    fill="none",
                    stroke="red",
                    stroke_width=10,
                ),
            ],
        )

        os.makedirs(os.path.dirname(outfile), exist_ok=True)
        
        if Path(outfile).is_file():
            outcount = 0
            while Path(outfile).is_file():
                outcount += 1
                outfile = f"out/output{outcount}.svg"

        with open(outfile, "w", encoding="utf-8") as file:
            file.write(str(canvas))

    def _process_cell(self, cell, d, prev_dir, start):
        if "dir" in cell:
            dir = cell["dir"]
        else:
            dir = prev_dir

        if cell["symbol"] == '╰' or cell["symbol"] == ['╰', '└']:
            if dir == "right":
                d.append(svg.q(0, self.cell_height / 2, self.cell_width / 2, self.cell_height / 2))
            elif dir == "up":
                d.append(svg.q(0-self.cell_width / 2, 0, 0-self.cell_width / 2, 0-self.cell_height / 2))
        elif cell["symbol"] == '└':
            if dir == "right":
                d.append(svg.v(self.cell_height / 2))
                d.append(svg.h(self.cell_width / 2))
            elif dir == "up":
                d.append(svg.h(0-self.cell_width / 2))
                d.append(svg.v(0-self.cell_height / 2))
        elif cell["symbol"] == '╮' or cell["symbol"] == ['╮', '┐']:
            if dir == "down":
                if (start):
                    d.append(svg.m(0-self.cell_height/2, self.cell_height/2))
                    d.append(svg.h(self.cell_height/2))
                d.append(svg.q(self.cell_width / 2, 0, self.cell_width / 2, self.cell_height / 2))
            elif dir == "left":
                d.append(svg.q(0, 0-self.cell_height / 2, 0-self.cell_width / 2, 0-self.cell_height / 2))
        elif cell["symbol"] == '╭' or cell["symbol"] == ['╭','┌']:
            if dir == "down":
                d.append(svg.q(0-self.cell_width / 2, 0, 0-self.cell_width / 2, self.cell_height / 2))
            elif dir == "right":
                d.append(svg.q(0, 0-self.cell_height / 2, self.cell_width / 2, 0-self.cell_height / 2))
        elif cell["symbol"] == '╯' or cell["symbol"] == ['╯','┘']:
            if dir == "left":
                d.append(svg.q(0, self.cell_height / 2, 0-self.cell_width / 2, self.cell_height / 2))
            elif dir == "up":
                d.append(svg.q(self.cell_width / 2, 0, self.cell_width / 2, 0-self.cell_height / 2))
        elif cell["symbol"] == '─':
            if dir == "right":
                d.append(svg.h(self.cell_width))
            elif dir == "left":
                d.append(svg.h(0-self.cell_width))
        elif cell["symbol"] == '│':
            if dir == "down":
                d.append(svg.v(self.cell_height))
            elif dir == "up":
                d.append(svg.v(0-self.cell_height))
        elif cell["symbol"] == '╷':
            if dir == "down":
                d.append(svg.m(0, self.cell_height/2))
                d.append(svg.v(self.cell_height/2))
            elif dir == "up":
                d.append(svg.v(0-self.cell_height/2))
        elif cell["symbol"] == '╵':
            if dir == "up":
                d.append(svg.m(0, 0-self.cell_height/2))
                d.append(svg.v(0-self.cell_height/2))
            elif dir == "down":
                d.append(svg.v(self.cell_height/2))
        elif cell["symbol"] == '╴':
            if dir == "left":
                d.append(svg.m(0-self.cell_width, 0))
                d.append(svg.h(0-self.cell_width))
            elif dir == "right":
                d.append(svg.v(self.cell_height/2))
        elif cell["symbol"] == '╶':
            if dir == "right":
                d.append(svg.m(self.cell_width/2, 0))
                d.append(svg.h(self.cell_width))
            elif dir == "left":
                d.append(svg.v(0-self.cell_height/2))

        return dir
