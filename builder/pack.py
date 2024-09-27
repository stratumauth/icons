import os

from builder.icon_pack_pb2 import IconPack
from builder.log import LOG
from builder.text import slug


def add_png_files_to_pack(pack: IconPack, build_dir: str):
    files = os.listdir(build_dir)
    added = []

    for file_name in files:
        name = slug(file_name.replace(".png", ""))

        if name in added:
            LOG.warning("Duplicate icon in pack %s", name)
            continue

        added.append(name)

        icon = pack.icons.add()
        icon.name = name

        icon_path = os.path.join(build_dir, file_name)

        with open(icon_path, "rb") as file:
            icon.data = file.read()
