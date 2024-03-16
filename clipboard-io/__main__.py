from .template import Template
from .node_clipboard import NodeClipboard

from . import template_utils

# template = Template("/home/parker/Downloads/CPIO_Files/SOP_Pighead/SOP_copy.cpio")
# template.unpack(output="/home/parker/Downloads/CPIO_Files/SOP_Pighead/output", make_dirs=True)

# template_path = "/home/parker/Downloads/CPIO_Files/SOP_Pighead/SOP_copy.cpio"
template_path = "/home/parker/Downloads/CPIO_Files/SOP_Multifiles/SOP_copy.cpio"
# template_path = "/home/parker/Downloads/CPIO_Files/LOP_EditLightNode/LOP_copy.cpio"

node_clip = NodeClipboard(template=template_path, clean_tmp=True)

node_clip.list_file_contents()

nodes = node_clip.get_nodes()
print("nodes:", nodes)

for node in nodes:
    parm = node.get_parm("uniformscale")
    print("PARM", parm)
    if(parm):
        print(node, "has parm")
        parm.set("5")
    else:
        print(node, "doesn't have parm")
    # node.add_parm(parm)

    # for parm in node.get_parms():
        # parm.set(["foo", "bar"])
        # print(parm)

node_clip.pack()
