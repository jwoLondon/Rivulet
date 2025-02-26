from riv_svg_generator import SvgGenerator


ColorSets = {
    "default": SvgGenerator.Parameters({
        "bg_pattern": SvgGenerator.BgPattern['dots'], 
        "bg_color": "#ffffff", 
        "color_set": ["#000000","#5f5ff6","#61d43f","#0000f5","#560c5c","#275e83","#666666"],
        "stroke_linecap": "round"
    }),
    
    "lavender": SvgGenerator.Parameters({
        "bg_pattern": SvgGenerator.BgPattern['blank'], 
        "bg_color": "#e0d0f4", 
        "color_set": ["#333333","#5f5ff6","#5AA87B","#0000f5","#560c5c","#9915A2"],
        "stroke_linecap": "square"
    }),

    "rain": SvgGenerator.Parameters({
        "bg_pattern": SvgGenerator.BgPattern['blank'], 
        "bg_color": "#aaaaaa", 
        "color_set": ["#333333","#C7D8F2","#8762A7","#0000f5","#3b4a8c"],
        "stroke_linecap": "round",
        "glyph_marker": "#C7D8F2"
    }),

    "solar": SvgGenerator.Parameters({
        "bg_pattern": SvgGenerator.BgPattern['lines'],
        "bg_color": "#faf4e0",
        "color_set": ["#85b2a7","#9f7e20","#6369b8","#ad4276","#616f77"],
        "line_color": "#3e3e3e",
        "stroke_linecap": "square"
    }),

    "vapor": SvgGenerator.Parameters({
        "bg_pattern": SvgGenerator.BgPattern['lines'],
        "bg_color": "#241f32",
        "color_set": ["#d3d9da","#9cd0da","#a97427","#d045a1","#444d60","#f3e894"],
        "line_color": "#7561b0",
        "line_opacity": 0.7,
        "stroke_linecap": "round"
    }),

    "test": SvgGenerator.Parameters({
        "bg_pattern": SvgGenerator.BgPattern['blank'],
        "bg_color": "#86BBD8",
        "color_set": ["#33658A","#F6AE2D","#2F4858","#F26419"],
        "stroke_linecap": "square"
    }),
}

