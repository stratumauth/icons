import glob
import tempfile
from os import path

from util import icon_pack_pb2
from util.git import clone_repo
from util.image import render_svg_as_png, optimise_png
from util.log import LOG
from util.pack import add_png_files_to_pack


class BasicBuildSettings:
    repo_url: str
    svg_glob: list[str]
    output_name: str
    pack_name: str
    pack_description: str
    pack_url: str


def process_icons(settings: BasicBuildSettings, pack_dir: str, build_dir: str):
    glob_path = path.join(pack_dir, *settings.svg_glob)
    icons = glob.glob(glob_path)

    for icon in icons:
        base_name = path.basename(icon)
        output_path = path.join(build_dir, base_name.replace("svg", "png"))

        with open(icon, "r") as file:
            svg = file.read()
            render_svg_as_png(svg, output_path)

        optimise_png(output_path)


def build_pack(settings: BasicBuildSettings, build_dir: str):
    pack = icon_pack_pb2.IconPack()
    pack.name = settings.pack_name
    pack.description = settings.pack_description
    pack.url = settings.pack_description

    add_png_files_to_pack(pack, build_dir)
    output_path = f"{settings.output_name}.iconpack"

    with open(output_path, "wb") as file:
        file.write(pack.SerializeToString())


def build_basic_pack(settings: BasicBuildSettings):
    with tempfile.TemporaryDirectory() as pack_dir:
        LOG.info("Cloning source icons from %s", settings.repo_url)
        clone_repo(settings.repo_url, pack_dir)

        with tempfile.TemporaryDirectory() as build_dir:
            LOG.info("Converting icons to png")
            process_icons(settings, pack_dir, build_dir)

            LOG.info("Building pack")
            build_pack(settings, build_dir)

    LOG.info("Written to %s", settings.output_name)
