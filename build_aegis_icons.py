#!/usr/bin/env python3

from builder.basic_builder import BasicBuildSettings, build_basic_pack


def main():
    settings = BasicBuildSettings()
    settings.repo_url = "https://github.com/aegis-icons/aegis-icons.git"
    settings.svg_glob = ["icons", "**", "*.svg"]
    settings.output_name = "aegis-icons"
    settings.pack_name = "Aegis Icons"
    settings.pack_description = "Unofficial monochrome-styled 2FA icons for open source Android authenticator Aegis"
    settings.pack_url = "https://github.com/aegis-icons/aegis-icons"

    build_basic_pack(settings)


if __name__ == "__main__":
    main()
