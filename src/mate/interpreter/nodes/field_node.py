from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp
from som.vmobjects.integer import Integer

class MateFieldReadNode(MateNode):

	def execute(self, frame):

		receiver = self._som_node.get_receiver(frame)
		value = self.do_mate_semantics(frame, receiver, [Integer(self._som_node.field_idx())])

		if value is None:
			return self._som_node.execute_prevaluated(frame, [receiver])
		else:
			return value

	def reflectiveOp(self):
		return ReflectiveOp.ExecutorReadField


class MateFieldWriteNode(MateNode):

	def execute(self, frame):

		receiver = self._som_node.get_receiver(frame)
		write_value = self._som_node.value(frame)

		value = self.do_mate_semantics(frame, receiver, [Integer(self._som_node.field_idx()), write_value])

		if value is None:
			return self._som_node.execute_prevaluated(frame, [receiver, write_value])
		else:
			return value

	def reflectiveOp(self):
		return ReflectiveOp.ExecutorWriteField
