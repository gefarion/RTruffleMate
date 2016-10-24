from som.interpreter.nodes.global_read_node import UninitializedGlobalReadNode
from som.interpreter.nodes.global_read_node import CachedGlobalReadNode
from som.interpreter.nodes.global_read_node import ConstantGlobalReadNode


class MateUninitializedGlobalReadNode(UninitializedGlobalReadNode):

    @classmethod
    def mateify(cls, node):
        return cls(node._global_name, node._universe, node._source_section)


class MateCachedGlobalReadNode(CachedGlobalReadNode):
    pass


class MateConstantGlobalReadNode(ConstantGlobalReadNode):
    pass