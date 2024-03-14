from . import template_utils

class Template():
    def __init__(self, path: str):
        self.cpio_path = path

    def unpack(self,
               output: None | str = None):
        template_utils.unpack_template(self.cpio_path, output=output)
