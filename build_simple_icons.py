#!/usr/bin/env python3

import glob
import json
import re
import tempfile
from os import path

from builder import icon_pack_pb2
from builder.git import clone_repo
from builder.image import render_svg_as_png, optimise_png, get_tinted_svg
from builder.log import LOG
from builder.pack import add_png_files_to_pack
from builder.text import slug

from typing import Callable

REPO_URL = "https://github.com/simple-icons/simple-icons.git"


def get_slugs(pack_dir: str) -> dict[str, str]:
    table_path = path.join(pack_dir, "slugs.md")
    result = {}

    expr = re.compile(r"\| `(.*?)` \| `(.*?)` \|")

    with open(table_path, "r") as file:
        md = file.read()

        for match in expr.finditer(md):
            result[match.group(1)] = match.group(2)

    return result


def get_icon_tints(pack_dir: str) -> dict[str, str]:
    slugs = get_slugs(pack_dir)
    data_path = path.join(pack_dir, "_data", "simple-icons.json")
    result = {}

    with open(data_path, "r") as file:
        data = json.load(file)

        for icon in data:
            title = icon["title"]

            if title in slugs:
                result[slugs[title]] = icon["hex"]

    return result


def tint_and_convert_icon(input_path: str, output_path: str, colour: str):
    svg = get_tinted_svg(input_path, colour)
    render_svg_as_png(svg, output_path)
    optimise_png(output_path)


def process_icons(pack_dir: str, build_dir: str, processor: Callable[[str, str], None]):
    glob_path = path.join(pack_dir, "icons", "*.svg")
    icons = glob.glob(glob_path)

    for icon in icons:
        base_name = path.basename(icon)
        output_path = path.join(build_dir, base_name.replace("svg", "png"))
        processor(icon, output_path)


def process_icons_monochrome(pack_dir: str, build_dir: str, colour: str):
    process_icons(
        pack_dir,
        build_dir,
        lambda input_path, output_path: tint_and_convert_icon(
            input_path, output_path, colour
        ),
    )


def process_icons_tinted(pack_dir: str, build_dir: str):
    tints = get_icon_tints(pack_dir)

    def processor(input_path, output_path):
        icon_name = slug(path.basename(input_path).replace(".svg", ""))

        if icon_name not in tints:
            LOG.warning("Cannot find slug for %s", icon_name)
            return

        tint = tints[icon_name]
        tint_and_convert_icon(input_path, output_path, tint)

    process_icons(pack_dir, build_dir, processor)


def build_pack(build_dir: str, output_path: str, suffix: str):
    pack = icon_pack_pb2.IconPack()
    pack.name = f"Simple Icons ({suffix})"
    pack.description = "Icons for popular brands"
    pack.url = "https://github.com/simple-icons/simple-icons"

    add_png_files_to_pack(pack, build_dir)

    with open(output_path, "wb") as file:
        file.write(pack.SerializeToString())


def build_pack_variant(suffix: str, processor: Callable[[str], None]):
    with tempfile.TemporaryDirectory() as build_dir:
        output_path = f"simple-icons-{suffix}.iconpack"

        LOG.info("Converting icons to png")
        processor(build_dir)

        LOG.info("Building pack")
        build_pack(build_dir, output_path, suffix)

        LOG.info("Written to %s", output_path)


def main():
    with tempfile.TemporaryDirectory() as pack_dir:
        LOG.info("Cloning source icons from %s", REPO_URL)
        clone_repo(REPO_URL, pack_dir)

        LOG.info("Building black variant")
        build_pack_variant(
            "black",
            lambda build_dir: process_icons_monochrome(pack_dir, build_dir, "000000"),
        )

        LOG.info("Building white variant")
        build_pack_variant(
            "white",
            lambda build_dir: process_icons_monochrome(pack_dir, build_dir, "ffffff"),
        )

        LOG.info("Building tinted variant")
        build_pack_variant(
            "tinted", lambda build_dir: process_icons_tinted(pack_dir, build_dir)
        )


if __name__ == "__main__":
    main()
