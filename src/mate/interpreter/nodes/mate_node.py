from som.interpreter.nodes.expression_node import ExpressionNode
from mate.interpreter.mop import MOPDispatcher
from mate.vm.constants import ReflectiveOp
from som.vmobjects.object import Object
import som.vm.universe
from mate.interpreter.nodes.lookup import UninitializedMateLookUpNode

class MateNode(ExpressionNode):

    _immutable_fields_ = ["_som_node?", "_lookup_node?"]
    _child_nodes_ = ["_som_node", "_lookup_node"]

    def __init__(self, som_node, source_section = None):
        ExpressionNode.__init__(self, source_section)
        som_node.replace(self)
        self._som_node = self.adopt_child(som_node)
        self._lookup_node = self.adopt_child(UninitializedMateLookUpNode(self.reflective_op(), som.vm.universe.get_current()))

    def get_meta_args(self, frame):
        raise NotImplementedError("Subclass must implement this method")

    def replace_lookup_list_head(self, node):
        self._lookup_node.replace(node)

    def execute(self, frame):

        value = None
        if not frame.meta_level():
            value = self.do_mate_semantics(frame)

        if value is None:
            return self._som_node.execute(frame)
        else:
            return value

    def do_mate_semantics(self, frame):
        assert frame is not None

        receiver = frame.get_self()
        environment = frame.get_meta_object_environment() or receiver.get_meta_object_environment()

        # No esta definido o es Nil
        if environment is None or not isinstance(environment, Object):
            return None

        method = self._lookup_node.lookup_meta_invokable(environment)
        if method is None:
            # El mate enviroment no define el methodo correspondiente a este nodo
            return None

        args = self.get_meta_args(frame)

        return method.invoke(receiver, args,  True)
