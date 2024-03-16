import subprocess, platform
import tempfile, os, shutil
from .template import Template
from .node import Node
from . import template_utils

class NodeClipboard():
    def __init__(self, template: Template | str, clean_tmp=True):
        self.clean_tmp=clean_tmp
        self.temp_dir=None
        # get template object
        if isinstance(template, str):
            self.template = Template(template)
        else:
            self.template = template

        self.is_unpacked=False
        self.unpack_template()
        self.houdini_tmp=self.get_houdini_tmp()

        # init
        self.init_node_type()

        self.nodes = []

        self.init_op_def()
        self.init_nodes()

    def init_node_type(self):
        if not self.contents_dir:
            raise Exception("content directory not found")
        node_type_path = os.path.join(self.contents_dir, "node_type")
        with open(node_type_path, "r") as f:
            self.node_type = f.read().lower().strip()
        
        # set export file
        out_file_name = self.node_type.upper()+"_copy.cpio"
        self.pack_export_file = os.path.join(self.houdini_tmp, out_file_name)

    def get_houdini_tmp(self):
        os = platform.system()
        if os == "Windows":
            raise Exception("windows functionality not implemented yet")
        elif os == "Linux":
            return r"/tmp/houdini_temp/"
        else:
            raise Exception("unkown os:", os)

    def unpack_template(self, force: bool=False):
        if self.is_unpacked and not force:
            return

        print("Unpacking template")
        temp_dir = tempfile.mkdtemp(prefix="hclipboard-io_", suffix="_"+self.template.name)
        print("New tmp file:", temp_dir)
        self.temp_dir = temp_dir
        self.template.unpack(output=temp_dir)
        self.content_register_dir = self.template.content_register_dir
        self.contents_dir = self.template.contents_dir
        print("contents_dir", self.template.contents_dir)
        self.is_unpacked=True

    def init_op_def(self):
        
        op_def_path = os.path.join(self.contents_dir, ".OPdummydefs")
        for section in template_utils.extract_ascii_strings(op_def_path).split("INDX"):
            print("\n\n\n\n\nSPLITTER")
            lines = section.split("\n")
            if len(lines)>7:
                name_line = lines[7].strip()
                if not name_line.startswith("name"):
                    continue
                name = name_line.split("\t")[1]
                print("NAME:",name)

    def list_file_contents(self):
        print("contents:", os.listdir(self.template.contents_dir))

    def clear_tmp(self):
        print("Removing tmp dir:", self.temp_dir)
        if(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def get_nodes(self):
        return self.nodes

    def init_nodes(self):
        files = os.listdir(self.template.contents_dir)
        for file in files:
            suffix = ".init"
            if file.endswith(suffix):
                # node_name = file[:-len(suffix)]
                
                contents_dir = self.template.contents_dir
                if not contents_dir:
                    raise Exception("Content dir not set, try unpacking fore fetching value")
                node_path = os.path.join(contents_dir, file)
                print("ADDING NODE AT PATH", node_path)
                new_node = Node(path=node_path)
                self.nodes.append(new_node)

    def pack(self):
        for node in self.nodes:
            node.export()

        print("packing ocio archive")
        os.chdir(self.contents_dir)
        pack_output = self.pack_export_file
        args = ["hcpio", "-F", self.content_register_dir, "-oO", pack_output, "-H", "odc"]
        print("args:", args)
        subprocess.run(args)
        pass

    def export_to_clipboard(self):

        pass

    def export_to_path(self, path: str):
        pass

    def __del__(self):
        if self.clean_tmp and self.temp_dir:
            self.clear_tmp()
        pass
