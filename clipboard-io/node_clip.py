from .template import Template

class NodeClip():
    def __init__(self, template: Template):
        self.template = template
        pass

    def checkout_template(self):
        self.template.checkout()

