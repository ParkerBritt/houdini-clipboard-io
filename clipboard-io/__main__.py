from .template import Template
from .node_clipboard import NodeClipboard

# template = Template("/home/parker/Downloads/CPIO_Files/SOP_Pighead/SOP_copy.cpio")
# template.unpack(output="/home/parker/Downloads/CPIO_Files/SOP_Pighead/output", make_dirs=True)

# template_path = "/home/parker/Downloads/CPIO_Files/SOP_Pighead/SOP_copy.cpio"
# template_path = "/home/parker/Downloads/CPIO_Files/SOP_Multifiles/SOP_copy.cpio"
template_path = "/home/parker/Downloads/CPIO_Files/LOP_EditLightNode/LOP_copy.cpio"

node_clip = NodeClipboard(template=template_path)

node_clip.list_file_contents()

nodes = node_clip.get_nodes()

for node in nodes:
    for parm in node.get_parms():
        parm.set(["foo", "bar"])
        print(parm)

