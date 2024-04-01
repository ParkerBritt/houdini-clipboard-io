from typing import List, Union, Optional, Dict
import re
import subprocess, platform, logging
import tempfile, os, shutil
from .template import Template
from .node import Node
from . import template_utils
from .parm import Parm
from .node_definition import NodeDefinition
from .parm_definition import ParmDefinition
logger = logging.getLogger(__name__)

class NodeClipboard():
    def __init__(self, template: Union[Template, str], clean_tmp=True):
        self.clean_tmp=clean_tmp
        self.temp_dir=None
        # get template object
        if isinstance(template, str):
            self.template = Template(template)
        else:
            self.template = template

        self.node_definitions: Dict[str, NodeDefinition] = {}
        self.is_unpacked=False
        self.unpack_template()
        self.houdini_tmp=self.get_houdini_tmp()

        # init
        self.init_node_type()

        self.nodes = []

        self.init_op_def()
        self.init_nodes_definitions()
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
            
        self.op_dummy_def = template_utils.extract_ascii_strings(op_def_path)
        with open("/home/parker/opdef_dump.txt", "w") as f:
            f.write(self.op_dummy_def)


    def list_file_contents(self):
        print("contents:", os.listdir(self.template.contents_dir))

    def clear_tmp(self):
        print("Removing tmp dir:", self.temp_dir)
        if(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def get_nodes(self):
        return self.nodes

    def init_nodes_definitions(self):
        print("initiating nodes")
        node_sections = re.findall(r"(?<=^ {4})name[\s\S]+?(?:(?=^})|\Z)", self.op_dummy_def, re.M)
        # node_sections = re.findall(r"(?<=^\s{4})name", self.op_dummy_def, re.M)
        for section in node_sections:
            # node name
            node_name = re.search(r"(?<=^name\t)\S+", section, re.M)
            if not node_name:
                raise Exception("Couldn't find name for node section:\n"+section)
            node_name = node_name.group()

            node_type = re.search
            logger.debug(f"ATTEMPTING TO CREATE NODE: {node_name}")
            node_type_search = re.search(r"(?P<type>\w+op)/"+node_name, self.op_dummy_def)
            if not node_type_search:
                raise Exception("couldn't find node type for:", node_name)
            node_type = node_type_search.group("type").lower()
            logger.debug(f"node type: {node_type}")

            # skip vops since they're unsupported
            if node_type == "vop":
                logger.debug(f"disregarding {node_type} node")
                continue
            
            # make node defition
            new_node_definition = NodeDefinition(node_name, node_type)
            self.node_definitions[node_name] = new_node_definition
        

            # make node
            # new_node = Node(node_name, parent=self)
            # self.nodes.append(new_node)

            # paramer values:
            parameter_raw_values = re.findall(r"(?<=^ {4}parm {\n)[\s\S]+?(?=\n^ {4}})", section, re.M)
            for values in parameter_raw_values:
                parm_name =  re.search(r"(?<=name {4}\")[^\n]+(?=\")", values)
                if not parm_name:
                    raise Exception(f"cannot file parm name for {parameter_raw_values}")
                parm_name = parm_name.group()
                # parm_line = re.findall(r" {8}\w+(\s+{)?(?(1)[\S\s]+?(?<=})|[\S\s]*?(?<=$))", values, re.M)
                parm_re_pattern = r" {8}\w+(\s+{)?(?(1)[\S\s]+?}|[\S\s]*?$)"
                matches = [match.group(0) for match in re.finditer(parm_re_pattern, values, re.MULTILINE)]
                parm_properties: dict = {}
                for line in matches:
                    property_list: list = line.strip().split(" ")
                    property_name: str = property_list[0]
                    property_value: str = " ".join(property_list[1:]).strip()
                    
                    # add item to list 
                    if property_name == "parmtag":
                        if not property_name in parm_properties:
                            parm_properties[property_name] = []
                        parm_properties[property_name].append(property_value)
                        continue

                    # add item directly
                    parm_properties[property_name] = property_value

                new_node_definition.add_parm_definition(parm_name, parm_properties)

    def init_nodes(self):
        files = os.listdir(self.template.contents_dir)
        for file in files:
            suffix = ".parm"
            if file.endswith(suffix):
                node_name = file[:-len(suffix)]
                
                contents_dir = self.contents_dir
                if not contents_dir:
                    raise Exception("Content dir not set, try unpacking fore fetching value")
                node_path = os.path.join(contents_dir, file)
                print("ADDING NODE AT PATH", node_path)
                new_node = Node(node_name, parent=self)
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
        for node in self.nodes:
            node.export()
        self.pack()
        

    def export_to_path(self, path: str):
        pass

    def __del__(self):
        if self.clean_tmp and self.temp_dir:
            self.clear_tmp()
        pass
