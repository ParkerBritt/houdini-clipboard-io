from .template import Template
from .node_clip import NodeClip

# template = Template("/home/parker/Downloads/CPIO_Files/SOP_Pighead/SOP_copy.cpio")
# template.unpack(output="/home/parker/Downloads/CPIO_Files/SOP_Pighead/output", make_dirs=True)

node_clip = NodeClip(template="/home/parker/Downloads/CPIO_Files/SOP_Pighead/SOP_copy.cpio")

node_clip.unpack_template()
