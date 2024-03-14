import os
from . import template_utils

class Template():
    def __init__(self, path: str):
        self.cpio_path = path
        self.nodes = []
        self.unpack_dir = None
        self.is_unpacked = False

        path_head, path_tail = os.path.split(self.cpio_path)
        self.file_name = path_tail
        self.name = os.path.splitext(path_tail)[0]
        self.contents_dir = None

    def unpack(self,
               output: str,
               make_dirs: bool = False):
        self.unpack_dir, self.contents_dir, self.content_register_dir = template_utils.unpack_template(
            self.cpio_path,
            output=output,
            make_dirs=make_dirs
        )
        self.unpack_dir = output
        self.is_unpacked = True
        self.contents_dir = os.path.join(self.unpack_dir, self.file_name+".dir")

