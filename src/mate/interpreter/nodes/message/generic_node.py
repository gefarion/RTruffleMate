from som.interpreter.nodes.message.generic_node import GenericMessageNode

class MateGenericMessageNode(GenericMessageNode):

    @classmethod
    def mateify(cls, node):
        return cls(
        	node._selector, node._universe, node._rcvr_expr,
        	node._arg_exprs, node._source_section
        )