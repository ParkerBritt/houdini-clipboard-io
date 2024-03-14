import os

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

    def get_parms(self):
        parm_read = ""
        with open(self.parm_path, "r", encoding="utf-8") as f:
            parm_read = f.read()

        # clear header and tail
        parm_lines = parm_read.split("\n")[2:-2]

        for line in parm_lines:
            print(line)
            

    def __str__(self):
        return "NODE:"+self.name

    def __repr__(self):
        return "NODE:"+self.name

