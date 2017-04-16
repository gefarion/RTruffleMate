from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp

class MateFieldReadNode(MateNode):

	def execute(self, frame):

		receiver = self._som_node.receiver(frame)
		value = self.doMateSemantics(frame, receiver)

		if value is None:
			return self._som_node.execute_evaluated(frame, receiver, None)
		else:
			return value

	def reflectiveOp(self):
		return ReflectiveOp.ExecutorReadField


class MateFieldWriteNode(MateNode):

	def execute(self, frame):

		receiver = self._som_node.receiver(frame)
		value = self.doMateSemantics(frame, receiver)

		if value is None:
			return self._som_node.execute_evaluated(frame, receiver, None)
		else:
			return value

	def reflectiveOp(self):
		return ReflectiveOp.ExecutorWriteField
