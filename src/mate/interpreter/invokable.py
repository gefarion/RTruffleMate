from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp
from som.interpreter.nodes.expression_node import ExpressionNode
from som.vmobjects.object import Object
from mate.interpreter.mop import MOPDispatcher
from som.vmobjects.array         import Array
import som.vm.universe
from mate.interpreter.nodes.lookup import UninitializedMateLookUpNode

class MateInvokable(MateNode):

    def __init__(self, som_node, source_section = None):
        ExpressionNode.__init__(self, source_section)
        som_node.get_method().set_invokable(self)
        self._som_node = self.adopt_child(som_node)
        self._lookup_node = self.adopt_child(UninitializedMateLookUpNode(self.reflective_op(), som.vm.universe.get_current()))

    def get_som_node(self):
        return self._som_node

    def invoke(self, receiver, arguments, meta_level):

        if meta_level:
            return self._som_node.invoke(receiver, arguments, meta_level)

        # Falta hacer llegar el frame
        environment = receiver.get_meta_object_environment()

        # No esta definido o es Nil
        if environment is None or not isinstance(environment, Object):
            return self._som_node.invoke(receiver, arguments, meta_level)

        method = self._lookup_node.lookup_meta_invokable(environment)
        if method is None:
            # El mate enviroment no define el methodo correspondiente a este nodo
            return self._som_node.invoke(receiver, arguments, meta_level)

        return method.invoke(receiver, [self._som_node.get_method(), Array.from_objects(arguments), environment], True)

    def reflective_op(self):
        return ReflectiveOp.MessageActivation