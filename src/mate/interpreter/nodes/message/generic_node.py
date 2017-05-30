from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp


class MateGenericMessageNode(MateNode):

	def reflective_op(self):
		return ReflectiveOp.MessageLookup