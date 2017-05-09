from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp
from som.vmobjects.integer import Integer

class MateFieldReadNode(MateNode):

	def reflective_op(self):
		return ReflectiveOp.ExecutorReadField


class MateFieldWriteNode(MateNode):

	def reflective_op(self):
		return ReflectiveOp.ExecutorWriteField
