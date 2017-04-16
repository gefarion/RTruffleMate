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

	def reflectiveOp(self):
		raise NotImplementedError("Subclasses need to implement reflectiveOp(self).")

	def MOPArguments(self):
		raise NotImplementedError("Subclasses need to implement MOPArguments(self).")

	# Retorna el enviroment con los meta objetos (por ahora solo soporta setearlo en el objeto)
	def getEnviromentMO(self, frame, receiver):
		assert receiver is not None
		assert frame is not None

		return receiver.get_meta_object_environment()

	def doMateSemantics(self, frame, receiver):
		assert receiver is not None
		assert frame is not None

		enviromentMO = self.getEnviromentMO(receivframe, receiver)
		if not enviromentMO:
			return None

		method = MOPDispatcher.lookupInvokable(self.reflectiveOp(), enviromentMO)
		if method is None:
			return None
		else:
			return method.invoke(receiver, self.MOPArguments())
