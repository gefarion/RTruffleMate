from som.interpreter.nodes.expression_node import ExpressionNode
from mate.interpreter.mop import MOPDispatcher
from mate.vm.constants import ReflectiveOp

class MateNode(ExpressionNode):

	_immutable_fields_ = ["_som_node?"]

	def __init__(self, som_node, source_section = None):
		ExpressionNode.__init__(self, source_section)
		self._som_node = som_node

	def execute(self, frame):
		if not self.mateOn():
			return self._som_node.execute(frame)

		if self.hasReceiver():
			receiver = self._som_node.receiver(frame)
			value = self.doMateSemantics(receiver, frame)

			if value is None:
				return self._som_node.executePreEvaluated(frame, receiver)
			else:
				return value			
		else:
			value = self.doMateSemantics(None, frame)

			if value is None:
				return self._som_node.execute(frame)
			else:
				return value

	def hasReceiver():
		return ReflectiveOp.hasReceiver(self.reflectiveOp())

	def mateOn(self):
		return False

	def reflectiveOp(self):
		# Debe ser implementado por las subclases
		raise NotImplementedError("Subclasses need to implement reflectiveOp(self).")

	# Retorna el enviroment con los meta objetos (por ahora solo soporta setearlo en el objeto)
	def getEnviromentMO(self, receiver, frame):
		if receiver:
			return receiver.get_meta_object_environment()
		else:
			return None	
		# En el futuro deberia quedar algo como: receiver.get_meta_object_environment() || frame.get_meta_object_environment()

	def MOPArguments(self):
		# Debe ser implementado por las subclases
		raise NotImplementedError("Subclasses need to implement MOPArguments(self).")

	def doMateSemantics(self, receiver, frame):
		enviromentMO = self.getEnviromentMO(receiver, frame)
		if not enviromentMO:
			return None

		method = MOPDispatcher.lookupInvokable(self.reflectiveOp(), enviromentMO)
		if method is None:
			return None
		else:
			return method.invoke(receiver, self.MOPArguments()) # TODO
