#!/usr/bin/env python3

from builder.basic_builder import BasicBuildSettings, build_basic_pack


def main():
    settings = BasicBuildSettings()
    settings.repo_url = "https://github.com/edent/SuperTinyIcons.git"
    settings.svg_glob = ["images", "svg", "*.svg"]
    settings.output_name = "super-tiny-icons"
    settings.pack_name = "Super Tiny Icons"
    settings.pack_description = (
        "Super Tiny Web Icons are minuscule versions of your favourite logos"
    )
    settings.pack_url = "https://github.com/edent/SuperTinyIcons"

    build_basic_pack(settings)


if __name__ == "__main__":
    main()
