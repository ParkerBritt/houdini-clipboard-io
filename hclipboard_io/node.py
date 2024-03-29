import os
from typing import List, Optional, Union
from .parm import Parm

class Node():
    def __init__(self, path: str):
        # self.path = path
        path_head, path_tail = os.path.split(path)
        self.name = os.path.splitext(path_tail)[0]
        self.path = path_head
        print("IN PATH", path)
        print("self.name", self.name)
        print("self.path", self.path)

        self.parm_path = os.path.join(self.path, self.name+".parm")
        # print("HEAD", self.path, "tail", self.name)

        if not os.path.exists(self.parm_path):
            raise Exception(f"Could not find .parm component of {self.name} parm at: {self.parm_path}")

        # don't populate parms until a query is made
        self.parms_populated = False
        self.parms = []

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
    
    def insert_parm(self, index: int, parm: Parm) -> None:
        self.parms.insert(index, parm)


    def init_parms(self) -> None:
        print("initiating parmameters")
        parm_read = ""
        with open(self.parm_path, "r", encoding="utf-8") as f:
            parm_read = f.read()

        # clear header and tail
        parm_file_split = parm_read.split("\n")
        self.header = parm_file_split[:2]
        self.tail = parm_file_split[-2]
        parm_lines = parm_file_split[2:-2]

        for line in parm_lines:
            line_parts = line.split("\t")

            name = line_parts[0]
            args = line_parts[4:-1]

            # print(f"name: {name}, args: {args}")
            # print(line)

            parm = Parm(name, args)
            self.parms.append(parm)

            self.parms_populated = True

    def export(self):
        export = "\n".join(self.header)
        formated_parms = ""
        for parm in self.parms:
            formated_parms+="\n"+parm.export()
        export += formated_parms
        export += "\n"+self.tail

        print("EXPORT:", export)
        parm_out_path = os.path.join(self.path, self.name+".parm")
        with open(parm_out_path, "w") as f:
            f.write(export)
            

    def __str__(self):
        return "NODE:"+self.name

    def __repr__(self):
        return "NODE:"+self.name

