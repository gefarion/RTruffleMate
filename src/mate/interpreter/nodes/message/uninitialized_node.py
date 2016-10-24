from som.interpreter.nodes.message.uninitialized_node import UninitializedMessageNode

class MateUninitializedMessageNode(UninitializedMessageNode):

	@classmethod
	def mateify(cls, node):
		return cls(
			node._selector,
			node._universe,
			node._rcvr_expr,
			node._arg_exprs,
            node._source_section
        )