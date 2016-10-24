from som.interpreter.nodes.field_node import FieldReadNode
from som.interpreter.nodes.field_node import FieldWriteNode

class MateFieldReadNode(FieldReadNode):

    @classmethod
    def mateify(cls, node):
        return cls(node._self_exp, node._field_idx, node._source_section)


class MateFieldWriteNode(FieldWriteNode):

    @classmethod
    def mateify(cls, node):
        return cls(node._self_exp, node._value_exp, node._field_idx, node._source_section)
