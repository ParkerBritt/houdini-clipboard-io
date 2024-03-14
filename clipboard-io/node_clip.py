import tempfile, os, shutil
from .template import Template

class NodeClip():
    def __init__(self, template: Template | str):
        # get template object
        if isinstance(template, str):
            self.template = Template("template")
        else:
            self.template = template

        self.is_unpacked=False
        self.temp_dir=None

    def unpack_template(self):
        temp_dir = tempfile.mkdtemp(prefix="hclipboard-io_", suffix="_"+self.template.name)
        print("New tmp file:", temp_dir)
        self.temp_dir = temp_dir
        # self.template.unpack(output=temp_dir)

    def clear_tmp(self):
        print("Removing tmp dir:", self.temp_dir)
        if(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def __del__(self):
        self.clear_tmp()
        

class Node():
    def __init__(self):
        pass
