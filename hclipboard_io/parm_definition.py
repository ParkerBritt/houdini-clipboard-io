import logging
from typing import Dict, Union, List, Optional
import re

logger = logging.getLogger(__name__)

class ParmDefinition():
    def __init__(self, name, properties: Dict[str, str]):
        self.name = name

        print("PROPERTIES", properties)
        # self.init_properties(properties)

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
