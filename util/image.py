import subprocess

import cairosvg

from util import ICON_SIZE


def render_svg_as_png(source: str, dest: str):
    cairosvg.svg2png(
        bytestring=source,
        write_to=dest,
        output_width=ICON_SIZE,
        output_height=ICON_SIZE,
    )


def get_tinted_svg(source: str, colour: str) -> str:
    with open(source, "r") as file:
        svg = file.read()
        return svg.replace("/></svg>", f' fill="#{colour}"/></svg>')


def optimise_png(path: str):
    optimisation = subprocess.run(
        ["oxipng", "-o", "4", "-i", "0", "--strip", "safe", path],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )

    if optimisation.stdout:
        message = optimisation.stdout.decode("utf-8")
        raise RuntimeError("Error calling oxipng command " + message)
