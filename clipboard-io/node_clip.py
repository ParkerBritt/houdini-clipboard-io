from .template import Template

class NodeClip():
    def __init__(self, template: Template):
        self.template = template
        pass

    def unpack_template(self):
        self.template.checkout()

class Node():
    def __init__(self):
        pass
