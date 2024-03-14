import os
from . import template_utils

class Template():
    def __init__(self, path: str):
        self.cpio_path = path
        self.unpack_dir = None
        self.is_unpacked = False

        path_head, path_tail = os.path.split(self.cpio_path)
        self.name = os.path.splitext(path_tail)[0]

    def unpack(self,
               output: str,
               make_dirs: bool = False):
        template_utils.unpack_template(
            self.cpio_path,
            output=output,
            make_dirs=make_dirs
        )
        self.unpack_dir = output
        self.is_unpacked = True
