from som.interpreter.nodes.expression_node import ExpressionNode

class MateNode(ExpressionNode):

	_immutable_fields_ = ["_som_node?"]

	def __init__(self, som_node, source_section = None):
		ExpressionNode.__init__(self, source_section)
		self._som_node = som_node

	def execute(self, frame):
		value = self.doMateSemantics(frame, [frame])
		if value is None:
			return self._som_node.execute(frame)
		else:
			return value

	def reflectiveOp(self):
		# Debe ser implementado por las subclases
		assert(0)

	def objectReflectiveMethod(self, frame, arguments):
		return None

	def environmentReflectiveMethod(self, frame):
		return None

	def reflectiveMethod(self, frame, arguments):
		return self.environmentReflectiveMethod(frame) or self.objectReflectiveMethod(frame, arguments)

	def doMateSemantics(self, frame, arguments=[]):
		method = self.reflectiveMethod(frame, arguments)

		if method is None:
			return None
		else:
			#return this.getMateDispatch().executeDispatch(frame, method, arguments);
			return None

