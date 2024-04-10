import os, logging, re
from typing import List, Optional, Union
from .parm import Parm
logger = logging.getLogger(__name__)

class Node():
    def __init__(self, name: str, parent):
        self.name = name
        self.path = parent.template.contents_dir
        self.parent_clipboard = parent
        logger.debug("ALL DEFS:", parent.node_definitions)

        self.component_files = [file for file in os.listdir(self.path) if file.startswith(self.name+".")]
        logger.debug("comonent files: {self.component_files}")

        self.parm_path = os.path.join(self.path, self.name+".parm")

        if not os.path.exists(self.parm_path):
            logger.debug("File Contents\n", os.listdir(self.path))
            raise Exception(f"Could not find .parm component of {self.name} parm at: {self.parm_path}")

        # don't populate parms until a query is made
        self.parms_populated = False
        self.parms = []

        self.init_type()

        self.node_definition = parent.node_definitions[self.type] 
        logger.debug(f"{self.name} NODE DEF: {self.node_definition}")

        # need definition first for init parms
        self.init_parms() # maybe lazy load these later

        logger.debug(f"node created\nname\t{self.name}\ntype\t{self.type}\n")

    def init_type(self) -> None:

        node_init_path = os.path.join(self.path, self.name+".init")
        with open(node_init_path, "r", encoding="utf-8") as f:
            init_read = f.read()

        # get .init file lines
        node_init_split = init_read.split("\n")
        # safety check
        if len(node_init_split) == 0: 
            raise Exception("{self.name}.init file empty")

        # get node type
        type_search = re.search(r"(?<=type = )[\S\s]+?$", node_init_split[0])
        # safety check
        if not type_search:
            raise Exception("couldn't find type for node: {self.name}")
        self.type = type_search.group()

    def delete(self) -> None:
        parent = self.parent_clipboard
        for file in self.component_files:
            file_path = os.path.join(self.path, file)
            if not os.path.exists(file_path):
                logger.warning(f"Could not delete file, file does not exists: {file_path}")
                continue
            logger.debug(f"Deleting file: {file_path}")
            os.remove(file_path)

        # delete file references from register
        with open(parent.content_register_dir, "r") as f:
            f_split = f.read().split("\n")
            f_split = [line for line in f_split if not line in self.component_files]

        with open(parent.content_register_dir, "w") as f:
            f.write("\n".join(f_split))
                    
        # delete node reference from clipboard
        for i, node in enumerate(self.parent_clipboard.nodes):
            if node == self:
                self.parent_clipboard.nodes.pop(i)
                break

    def get_parms(self) -> List[Parm]:
        if not self.parms_populated:
            self.init_parms()

        return self.parms

    def get_parm(self, search_name: str) -> Optional[Parm]:
        if not self.parms_populated:
            self.init_parms()

        for parm in self.parms:
            if parm.name == search_name:
                return parm

        return None

    def add_parm(self, parm: Parm) -> None:
        self.parms.append(parm)

    def set_parm(self, parm_name: str, parm_val):
        self.get_parm(parm_name).set(parm_val)
    
    def insert_parm(self, index: int, parm: Parm) -> None:
        self.parms.insert(index, parm)

    # def init_parms(self) -> None:
    #     parm_read = ""
    #     with open(self.parm_path, "r", encoding="utf-8") as f:
    #         parm_read = f.read()
    #     self.version = float(re.search(r"(?<=version )[\d.]+", parm_read).group())
    #     print("version:", version)
    #
    #     # op_def = self.parent_clipboard.op_dummy_def

        

    def init_parms(self) -> None:
        logger.debug("initiating parmameters")
        parm_read = ""
        with open(self.parm_path, "r", encoding="utf-8") as f:
            parm_read = f.read()

        # clear header and tail
        parm_file_split = parm_read.split("\n")
        self.parm_header = parm_file_split[:2]
        self.parm_tail = parm_file_split[-2]
        parm_lines = parm_file_split[2:-2]

        for line in parm_lines:
            line_parts = line.split("\t")

            name = line_parts[0]
            args = line_parts[4:-1]

            # print(f"name: {name}, args: {args}")
            # print(line)

            parm = Parm(name, "\t".join(args), parent=self)
            self.parms.append(parm)

            self.parms_populated = True

    def export(self):
        # head = "{\nversion "+self.version_num+"\n"
        # tail = "}"
        head, tail = (self.parm_header, self.parm_tail)
        formated_parms = ""
        for parm in self.parms:
            formated_parms+="\n"+parm.export_processing()
        export = f"\n{"\n".join(head)}\n{formated_parms}\n{tail}"

        logger.debug(f"EXPORT: {export}")
        parm_out_path = os.path.join(self.path, self.name+".parm")
        logger.debug(f"Writing parameters to {parm_out_path}")
        with open(parm_out_path, "w") as f:
            f.write(export)
            

    def __str__(self):
        return "NODE:"+self.name

    def __repr__(self):
        return "NODE:"+self.name

