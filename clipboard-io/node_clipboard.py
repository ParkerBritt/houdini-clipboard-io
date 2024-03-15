import tempfile, os, shutil
from .template import Template
from .node import Node

class NodeClipboard():
    def __init__(self, template: Template | str):
        # get template object
        if isinstance(template, str):
            self.template = Template(template)
        else:
            self.template = template

        self.is_unpacked=False
        self.temp_dir=None
        self.nodes = []

        self.unpack_template()
        self.init_nodes()

    def unpack_template(self):
        temp_dir = tempfile.mkdtemp(prefix="hclipboard-io_", suffix="_"+self.template.name)
        print("New tmp file:", temp_dir)
        self.temp_dir = temp_dir
        self.template.unpack(output=temp_dir)
        print("contents_dir", self.template.contents_dir)
        self.is_unpacked=True

    def list_file_contents(self):
        print("contents:", os.listdir(self.template.contents_dir))

    def clear_tmp(self):
        print("Removing tmp dir:", self.temp_dir)
        if(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def get_nodes(self):
        return self.nodes

    def init_nodes(self):
        if not self.is_unpacked:
            print("Cannot create nodes without unpacking first")
            print("Unpacking template now")
            self.unpack_template()

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


    def __del__(self):
        self.clear_tmp()
        pass
