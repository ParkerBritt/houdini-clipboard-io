from hclipboard_io import NodeClipboard
import logging
import argparse

logger = logging.basicConfig(level="WARNING")

parser = argparse.ArgumentParser(
        prog="Houdini Clipboard Edit",
        description="edit the houdini clipboard in the command line using flags"
        )
parser.add_argument("node", type=str)
parser.add_argument("parm", type=str)
parser.add_argument("val", type=str)
parser.add_argument("--context", type=str)

parser_args = parser.parse_args()
template_path = "/tmp/houdini_temp/SOP_copy.cpio"

clipboard = NodeClipboard(template=template_path, clean_tmp=True)

node = clipboard.get_node(parser_args.node)
node.set_parm(parser_args.parm, parser_args.val)

clipboard.export_to_clipboard()
#
