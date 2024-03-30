from typing import Union, List, Optional, Dict
import re

class Parm():
    def __init__(self, name, properties: Dict[str, str], value):
        self.name = name
        self.value = value 

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
        default = properties.get('default', None)
        if(default):
            default = re.search(r"-?\d+", default)
            if(default):
                default = int(default.group())
        self.default = default

        # range
        parm_range = properties.get('range', None)
        if(parm_range):
            parm_range  = re.findall(r"-?\d+", parm_range)
            parm_range = tuple(int(num) for num in parm_range)
        self.range = parm_range
        # parmtag
        self.parmtag = properties.get('parmtag', None)

        self.properties = [self.label, self.type, self.size, self.default, self.range, self.parmtag]

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

    def get_formatted_value(self, unformatted_value):
                # unhandled types:
            # angle
            # button
            # button strip
            # color
            # color and alpha
            # data
            # directional vector
            # file
            # file - directory
            # file- geometry
            # file - image
            # float vector 2
            # float vector 3
            # float vector 4
            # folder
            # geometry data
            # icon strip
            # key-value dictionary
            # label
            # label - heading
            # label -message
            # logarithmic float
            # logarithmic integer
            # min/max float
            # min/max integer
            # operator list
            # operator path
            # rgba mask
            # ramp (color)
            # ramp (float)
            # separator
            # spacer
            # toggle
            # uv
            # uvw
        # handled types
            # float
            # integer
            # string
            # ordered menu


        formatted_val: Union[int, tuple, str] = unformatted_value
        # format value
        if self.type in ("string", "ordinal"):
            formatted_val = f"\"{self.value}\""
        if self.type in ("vector", "color"):
            formatted_val = "\t".join(self.value)
        return formatted_val

    
    def export(self):
        name = self.name
        locks = "[ 0	locks=0 ]" # still need to figure this out

        formatted_val = self.get_formatted_value(self.value)
        export = name+"\t"+locks+"\t(\t"+formatted_val+"\t)"

        return export

    def __str__(self):
        return f"{self.name}:{self.properties}"
