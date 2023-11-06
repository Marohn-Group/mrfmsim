import mmodel
from mmodel.metadata import MetaDataFormatter, nodeformatter

_meta_order = [
    "name",
    "_",
    "node_func",
    "output",
    "output_unit",
    "functype",
    "modifiers",
    "_",
    "doc",
]
_format_dict = nodeformatter.format_dict.copy()
# switch display name to return_unit
_format_dict.update({"output_unit": lambda k, v: [f"return_unit: {v}"] if v else []})
mrfm_nodeformatter = MetaDataFormatter(
    _format_dict, _meta_order, nodeformatter.text_wrapper, ["modifiers"]
)


class Node(mmodel.Node):
    def __str__(self):
        """Modify the string representation to include unit."""
        return mrfm_nodeformatter(self)
