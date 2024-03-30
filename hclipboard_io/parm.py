from typing import Union, List, Optional, Dict
import re

class Parm():
    def __init__(self, name, properties: Dict[str, str]):
        self.name = name

        self.init_properties(properties)

    def init_properties(self, properties):
        # label
        label = properties.get('label', None)
        if(label):
            label = label.strip("\"")
        self.label = label
        # type
        self.type = properties.get('type', None)
        # size
        size = properties.get('size', None)
        if(size):
            self.size: int = int(size)
        self.size = size
        # default
        self.default = properties.get('default', None)
        # range
        parm_range = properties.get('range', None)
        if(parm_range):
            parm_range  = re.findall(r"-?\d+", parm_range)
            parm_range = tuple(int(num) for num in parm_range)
        self.range = parm_range
        # parmtag
        self.parmtag = properties.get('parmtag', None)

        self.properties = [self.label, self.type, self.size, self.default, self.range, self.parmtag]

        for prop in self.properties:
            print("\nname", self.name)
            print("label", self.label)
            print("type", self.type)
            print("size", self.size)
            print("default", self.default)
            print("range", self.range)
            print("parmtag", self.parmtag)

    def set(self, value: Union[str, int, float, List[Union[str,int,float]]], index: Optional[int]=None):
        arg_len = len(self.args)

        # single element inputs
        if isinstance(value, (str, int, float)):
            if index and index > arg_len:
                print(f"WARNING: setting value out of index range. Parm {self.name} Val {value} Max Args {arg_len}")
                self.args[index] = value
                return
            else:
                value = [value]
                self.args = value
                return

        # multi element input
        elif isinstance(value, (list, tuple)):
            # list inputs
            if len(value) > arg_len:
                print("WARNING: new parm {self.name} is longer than previous parm.",
                      f"NEW: {value}:{len(value)} old {self.args}:{arg_len}")
            self.args = value

        # unkown input
        else:
            print(f"WARNING: can't set parm {self.name} to type {type(value)}")

        return self
    
    def export(self):
        name = self.name
        locks = "[ 0	locks=0 ]"
        args = "\t".join(self.args)
        export = name+"\t"+locks+"\t(\t"+args+"\t)"

        return export

    def __str__(self):
        return f"{self.name}:{self.properties}"
