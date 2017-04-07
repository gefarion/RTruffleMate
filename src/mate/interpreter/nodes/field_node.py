from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp

class MateFieldReadNode(MateNode):

	def mateOn(self):
		return True

	def reflectiveOp(self):
		return ReflectiveOp.ExecutorReadField


class MateFieldWriteNode(MateNode):
	
	def mateOn(self):
		return True
	
	def reflectiveOp(self):
		return ReflectiveOp.ExecutorWriteField
