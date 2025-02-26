"Tool to create svg files from Rivulet source code"
from enum import Enum
import os
from pathlib import Path
import svg

class SvgGenerator:
    "Tool to create svg files from Rivulet source code"

    BgPattern = Enum('BackPattern', [('blank', 1), ('lines', 1), ('dots', 2)])

    class Parameters:
        "Parameter Set for SvgGenerator"
        def __init__(self):
            self.cell_width = 80
            self.cell_height = 100
            self.bg_pattern = SvgGenerator.BgPattern['lines']
            self.bg_color = "#ffffff"
            # self.bg_color = "#e0d0f4"
            self.color_set = ["#000000","#5f5ff6","#61d43f","#0000f5","#560c5c","#275e83","#666666"]
            self.stroke_width = 20

    def __init__(self, parameters=None):
        self.p = parameters
        if not parameters:
            self.p = SvgGenerator.Parameters()            

    def generate(self, parse_tree, outfile=False):
        "Generate an SVG file from the parse tree"
        if not outfile:
            outfile = "out/output.svg" # this should increment probly

        x_off = 0 # currently assumes vertical layout
        y_off = 1

        glyph_widths = []

        elements = []

        elements.append(svg.Rect(x=0, y=0, width="100%", height="100%", fill=self.p.bg_color))

        for g, glyph in enumerate(parse_tree):
            prev_dir = None
            widths = []
            x_off = 0
            for i in range(0, glyph["level"]):
                d = []
                d.append(svg.M(x_off * self.p.cell_width, y_off * self.p.cell_height))
                self._add_start_spacing(d, .5, 0)
                d.append(svg.v(self.p.cell_height/2))
                elements.append(
                    svg.Path(
                        d=d,
                        fill="none",
                        stroke="#999999",
                        stroke_width=self.p.stroke_width,
                    )
                )
                x_off += 1
            
            for idx, token in enumerate(glyph["tokens"]):
                d = []
                # move to upper left of starting cell
                d.append(svg.M((token["x"] + x_off) * self.p.cell_width, (token["y"] + y_off) * self.p.cell_height))
                widths.append(token["x"] + x_off)

                prev_dir = self._process_cell(token, d, prev_dir, True, widths)
                for c in token["cells"]:
                    prev_dir = self._process_cell(c, d, prev_dir, False, widths)
                if token["action"] is not None:
                    d.append(svg.M((token["action"]["x"] + x_off) * self.p.cell_width, (token["action"]["y"] + y_off) * self.p.cell_height))

                    prev_dir = self._process_cell(token["action"], d, prev_dir, True, widths)
                    for c in token["action"]["cells"]:
                        prev_dir = self._process_cell(c, d, prev_dir, False, widths)
                if "second" in token and token["second"] is not None:
                    d.append(svg.M((token["second"]["x"] + x_off) * self.p.cell_width, (token["second"]["y"] + y_off) * self.p.cell_height))

                    prev_dir = self._process_cell(token["second"], d, prev_dir, True, widths)
                    for c in token["second"]["cells"]:
                        prev_dir = self._process_cell(c, d, prev_dir, False, widths)
                glyph_widths.append(max(widths))

                elements.append(
                    svg.Path(
                        d=d,
                        fill="none",
                        stroke=self.p.color_set[idx % len(self.p.color_set)],
                        stroke_width=self.p.stroke_width,
                    )
                )

            y_off += (len(glyph["glyph"]) + 2)

        if self.p.bg_pattern == SvgGenerator.BgPattern['dots']:
            for y in range(0, y_off):
                for x in range(0, max(glyph_widths) + 4):
                    elements.append(svg.Circle(r=self.p.stroke_width/2, cx=(x + 0.5) * self.p.cell_width, cy=y * self.p.cell_height, fill="#000000", fill_opacity=0.1))

        elif self.p.bg_pattern == SvgGenerator.BgPattern['lines']:
            for y in range(0, y_off):
                elements.append(svg.Line(x1=0, y1=self.p.cell_height * y, x2=(max(glyph_widths) + 4) * self.p.cell_width, y2=self.p.cell_height * y, stroke="#000000", stroke_opacity=0.35, stroke_width=1))

        canvas = svg.SVG(
            width=(max(glyph_widths) + 4) * self.p.cell_width,
            height=y_off * self.p.cell_height,
            elements=elements,
            style="background-color:" + self.p.bg_color,
        )

        os.makedirs(os.path.dirname(outfile), exist_ok=True)
        
        if Path(outfile).is_file():
            outcount = 0
            while Path(outfile).is_file():
                outcount += 1
                outfile = f"out/output{outcount}.svg"

        with open(outfile, "w", encoding="utf-8") as file:
            file.write(str(canvas))

    def _add_start_spacing(self, d, x, y):
        d.append(svg.m(self.p.cell_width * x, self.p.cell_height * y))
    
    def _add_curve(self, d, x1, y1, x, y):
        # Draws a quadratic Bézier curve from the current point to (x,y)
        # with control point (x1,y1), each multiplied by half base cell size
        d.append(svg.q(self.p.cell_width * x1 / 2, self.p.cell_height * y1 / 2, self.p.cell_width * x / 2, self.p.cell_height * y / 2))


    def _process_cell(self, cell, d, prev_dir, start, widths):
        if "dir" in cell:
            dir = cell["dir"]
        else:
            dir = prev_dir

        # at start, each begins in the upper left of the corner. We need to move it to the appropriate entry point

        # rounded corners
        if cell["symbol"] == '╰' or cell["symbol"] == ['╰', '└']:
            if dir == "right":
                if start:
                    self._add_start_spacing(d, .5, 0)
                self._add_curve(d, 0, 1, 1, 1)
                widths.append(widths[-1] + 1)
            elif dir == "up":
                if start:
                    self._add_start_spacing(d, 1, .5)
                self._add_curve(d, -1, 0, -1, -1)
        elif cell["symbol"] == '╮' or cell["symbol"] == ['╮', '┐']:
            if dir == "down":
                if start:
                    self._add_start_spacing(d, 0, .5)
                self._add_curve(d, 1, 0, 1, 1)
            elif dir == "left":
                if start:
                    self._add_start_spacing(d, .5 ,1)
                self._add_curve(d, 0, -1, -1, -1)
                widths.append(widths[-1] - 1)
        elif cell["symbol"] == '╭' or cell["symbol"] == ['╭','┌']:
            if dir == "down":
                if start:
                    self._add_start_spacing(d, 1, .5)
                self._add_curve(d, -1, 0, -1, 1)
            elif dir == "right":
                if start:
                    self._add_start_spacing(d, .5, 1)
                self._add_curve(d, 0, -1, 1, -1)
                widths.append(widths[-1] + 1)
        elif cell["symbol"] == '╯' or cell["symbol"] == ['╯','┘']:
            if dir == "left":
                if start:
                    self._add_start_spacing(d, .5, 0)
                self._add_curve(d, 0, 1, -1, 1)
                widths.append(widths[-1] - 1)
            elif dir == "up":
                if start:
                    self._add_start_spacing(d, 0, .5)
                self._add_curve(d, 1, 0, 1, -1)


        # square corners
        elif cell["symbol"] == '┐':
            if dir == "down":
                if start:
                    self._add_start_spacing(d, 0, .5)
                d.append(svg.h(self.p.cell_width / 2))
                d.append(svg.v(self.p.cell_height / 2))
            elif dir == "left":
                if start:
                    self._add_start_spacing(d, 1, .5)
                d.append(svg.h(0-self.p.cell_width / 2))
                d.append(svg.v(0-self.p.cell_height / 2))
                widths.append(widths[-1] - 1)
        elif cell["symbol"] == '└':
            if dir == "right":
                if start:
                    self._add_start_spacing(d, .5, 0)
                d.append(svg.v(self.p.cell_height / 2))
                d.append(svg.h(self.p.cell_width / 2))
                widths.append(widths[-1] + 1)
            elif dir == "up":
                if start:
                    self._add_start_spacing(d, 1, .5)
                d.append(svg.h(0-self.p.cell_width / 2))
                d.append(svg.v(0-self.p.cell_height / 2))
        elif cell["symbol"] == '┌':
            if dir == "down":
                if start:
                    self._add_start_spacing(d, 1, .5)
                d.append(svg.h(0-self.p.cell_width / 2))
                d.append(svg.v(self.p.cell_height / 2))
            elif dir == "right":
                if start:
                    self._add_start_spacing(d, .5, 1)
                d.append(svg.v(0-self.p.cell_height / 2))
                d.append(svg.h(self.p.cell_width / 2))
                widths.append(widths[-1] + 1)
        elif cell["symbol"] == '┘':
            if dir == "left":
                if start:
                    self._add_start_spacing(d, .5, 0)
                d.append(svg.v(self.p.cell_height / 2))
                d.append(svg.h(0-self.p.cell_width / 2))
                widths.append(widths[-1] - 1)
            elif dir == "up":
                if start:
                    self._add_start_spacing(d, 0, .5)
                d.append(svg.h(self.p.cell_width / 2))
                d.append(svg.v(0-self.p.cell_height / 2))                          


        # straight lines
        elif cell["symbol"] == '─' or cell["symbol"] == ['─']:
            if dir == "right":
                d.append(svg.h(self.p.cell_width))
                widths.append(widths[-1] + 1)
            elif dir == "left":
                d.append(svg.h(0-self.p.cell_width))
                widths.append(widths[-1] - 1)
        elif cell["symbol"] == '│' or cell["symbol"] == ['│']:
            if dir == "down":
                if start:
                    self._add_start_spacing(d, .5, 0)
                d.append(svg.v(self.p.cell_height))
            elif dir == "up":
                if start:
                    self._add_start_spacing(d, .5, 1)
                d.append(svg.v(0-self.p.cell_height))
        elif cell["symbol"] == '╷' or cell["symbol"] == ['╷']:
            if dir == "down":
                self._add_start_spacing(d, 0, .5)
                d.append(svg.v(self.p.cell_height/2))
            elif dir == "up":
                if start:
                    self._add_start_spacing(d, .5, 1)
                d.append(svg.v(0-self.p.cell_height/2))
        elif cell["symbol"] == '╵' or cell["symbol"] == ['╵']:
            if dir == "up":
                self._add_start_spacing(d, 0, -.5)
                d.append(svg.v(0-self.p.cell_height/2))
            elif dir == "down":
                if start:
                    self._add_start_spacing(d, .5, 0)
                d.append(svg.v(self.p.cell_height/2))
        elif cell["symbol"] == '╴' or cell["symbol"] == ['╴']:
            if dir == "left":
                self._add_start_spacing(d, -0.5, 0)
                d.append(svg.h(0-self.p.cell_width))
                widths.append(widths[-1] - 1)
            elif dir == "right":
                self._add_start_spacing(d, .5, .5)
                d.append(svg.v(self.p.cell_height/2))
                widths.append(widths[-1] + 1)
        elif cell["symbol"] == '╶' or cell["symbol"] == ['╶']:
            if dir == "right":
                self._add_start_spacing(d, 0.5, 0)
                d.append(svg.h(self.p.cell_width))
            elif dir == "left":
                self._add_start_spacing(d, .5, .5)
                d.append(svg.v(0-self.p.cell_height/2))
                widths.append(widths[-1] - 1)

        return dir
