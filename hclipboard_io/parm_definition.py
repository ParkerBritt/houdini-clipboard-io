import logging
from typing import Dict, Union, List, Optional
import re

logger = logging.getLogger(__name__)

class ParmDefinition():
    def __init__(self, name, properties: Dict[str, str]):
        self.name = name

        self.init_properties(properties)

        logger.debug("New Parm Definition\n"+self.__repr__()+"\n")

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
        self.parmtags = properties.get('parmtag', None)

        self.properties = [self.label, self.type, self.size, self.default, self.range, self.parmtags]

    def __repr__(self):
        return f"""name\t{self.name}
label\t{self.label}
type\t{self.type}                     
size\t{self.size}
default\t{self.default}
range\t{self.range}
parmtag\t{self.parmtags}"""
