from typing import Union, List, Optional, Dict
import re

class Parm():
    def __init__(self, name, value, parent):
        self.name = name

        self.node = parent
        self.definition = self.node.node_definition.get_parm_definition(self.name)

        self.type = self.definition.type

        self.value = self.input_preprocessing(value) 

        # self.init_properties(self.raw_value)

    def input_preprocessing(self, value: str):
        out_val = value
        if self.type in ("string", "toggle", "ordinal"):
            out_val = value.strip('"')
        if self.type in ("vector"):
            out_val = value.split("\t")
        return out_val

    def export_processing(self) -> str:
        name = self.name
        locks = "[ 0	locks=0 ]" # still need to figure this out

        formatted_val = self.get_formatted_value(self.value)
        export = name+"\t"+locks+"\t(\t"+formatted_val+"\t)"

        return export

    def set(self, value: Union[str, int, float, List[Union[str,int,float]]], index: Optional[int]=None):
        self.value = value
        # arg_len = len(self.args)

        # # single element inputs
        # if isinstance(value, (str, int, float)):
        #     if index and index > arg_len:
        #         print(f"WARNING: setting value out of index range. Parm {self.name} Val {value} Max Args {arg_len}")
        #         self.args[index] = value
        #         return
        #     else:
        #         value = [value]
        #         self.args = value
        #         return
        #
        # # multi element input
        # elif isinstance(value, (list, tuple)):
        #     # list inputs
        #     if len(value) > arg_len:
        #         print("WARNING: new parm {self.name} is longer than previous parm.",
        #               f"NEW: {value}:{len(value)} old {self.args}:{arg_len}")
        #     self.args = value
        #
        # # unkown input
        # else:
        #     print(f"WARNING: can't set parm {self.name} to type {type(value)}")

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
        if self.type in ("string", "ordinal", "toggle"):
            formatted_val = f"\"{self.value}\""
        if self.type in ("vector", "color"):
            formatted_val = "\t".join((str(value) for value in unformatted_value))
        return formatted_val

    

    def __str__(self):
        return f"{self.name}:{self.properties}"

    def __repr__(self):
        return f"parm:{self.name}:{self.value}:{self.definition}"
