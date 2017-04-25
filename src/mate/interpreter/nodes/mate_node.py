from som.interpreter.nodes.expression_node import ExpressionNode
from mate.interpreter.mop import MOPDispatcher
from mate.vm.constants import ReflectiveOp

class MateNode(ExpressionNode):

	_immutable_fields_ = ["_som_node?"]

	def __init__(self, som_node, source_section = None):
		ExpressionNode.__init__(self, source_section)
		self._som_node = som_node

	def execute(self, frame):
		raise NotImplementedError("Subclasses need to implement execute(self, frame).")

	def reflective_op(self):
		raise NotImplementedError("Subclasses need to implement reflective_op(self).")

	def mop_arguments(self, frame):
		raise NotImplementedError("Subclasses need to implement mop_arguments(self).")

	def do_mate_semantics(self, frame, receiver, args):
		assert receiver is not None
		assert frame is not None

		environment = receiver.get_meta_object_environment() or frame.get_meta_object_environment()
		if not environment:
			return None

		method = MOPDispatcher.lookup_invokable(self.reflective_op(), environment)
		if method is None:
			return None
		else:
			return method.invoke(receiver, args)
