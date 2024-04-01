from typing import Dict
from .parm_definition import ParmDefinition

import logging

logger = logging.getLogger(__name__)

class NodeDefinition():
    def __init__(self, node_name, node_type):
        self.node_name = node_name
        self.node_type = node_type
        self.parm_definitions = {}
        logger.debug(f"created new node definition, name: {self.node_name}, type: {self.node_type}")

    def add_parm_definition(self, name: str, raw_properties: Dict[str, str]):
        new_parm =  ParmDefinition(name, raw_properties)
        self.parm_definitions[name] = new_parm

    def get_parm_definition(self, name):
        return self.parm_definitions.get(name, None)
