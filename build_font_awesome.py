#!/usr/bin/env python3

import glob
import tempfile
from os import path

from builder import icon_pack_pb2
from builder.git import clone_repo
from builder.image import render_svg_as_png, optimise_png, get_tinted_svg
from builder.log import LOG
from builder.pack import add_png_files_to_pack

REPO_URL = "https://github.com/FortAwesome/Font-Awesome.git"


def tint_and_convert_icon(input_path: str, output_path: str, colour: str):
    svg = get_tinted_svg(input_path, colour)
    render_svg_as_png(svg, output_path)
    optimise_png(output_path)


def process_icons(pack_dir: str, build_dir: str, colour: str):
    glob_path = path.join(pack_dir, "svgs", "brands", "*.svg")
    icons = glob.glob(glob_path)

    for icon in icons:
        base_name = path.basename(icon)
        output_path = path.join(build_dir, base_name.replace("svg", "png"))
        tint_and_convert_icon(icon, output_path, colour)


def build_pack(build_dir, output_path, suffix):
    pack = icon_pack_pb2.IconPack()
    pack.name = f"Font Awesome Brands ({suffix})"
    pack.description = "The iconic SVG, font, and CSS toolkit"
    pack.url = "https://github.com/FortAwesome/Font-Awesome"

    add_png_files_to_pack(pack, build_dir)

    with open(output_path, "wb") as file:
        file.write(pack.SerializeToString())


def build_pack_variant(pack_dir: str, suffix: str, colour: str):
    with tempfile.TemporaryDirectory() as build_dir:
        output_path = f"font-awesome-brands-{suffix}.iconpack"

        LOG.info("Converting icons to png")
        process_icons(pack_dir, build_dir, colour)

        LOG.info("Building pack")
        build_pack(build_dir, output_path, suffix)

        LOG.info("Written to %s", output_path)


def main():
    with tempfile.TemporaryDirectory() as pack_dir:
        LOG.info("Cloning source icons from %s", REPO_URL)
        clone_repo(REPO_URL, pack_dir)

        LOG.info("Building black variant")
        build_pack_variant(pack_dir, "black", "000000")

        LOG.info("Building white variant")
        build_pack_variant(pack_dir, "white", "ffffff")


if __name__ == "__main__":
    main()
