from som.interpreter.nodes.expression_node import ExpressionNode
from mate.interpreter.mop import MOPDispatcher
from mate.vm.constants import ReflectiveOp

class MateNode(ExpressionNode):

    _immutable_fields_ = ["_som_node?"]
    _child_nodes_ = ["_som_node"]

    def __init__(self, som_node, source_section = None):
        ExpressionNode.__init__(self, source_section)
        som_node.replace(self)
        self._som_node = self.adopt_child(som_node)

    def execute(self, frame):

        args = self._som_node.get_execute_args(frame)
        value = self.do_mate_semantics(frame, args)

        if value is None:
            return self._som_node.execute_prevaluated(frame, args)
        else:
            return value

    def reflective_op(self):
        raise NotImplementedError("Subclasses need to implement reflective_op(self).")

    def mop_arguments(self, frame):
        raise NotImplementedError("Subclasses need to implement mop_arguments(self).")

    def do_mate_semantics(self, frame, args):
        assert frame is not None

        environment = args[0].get_meta_object_environment() or frame.get_meta_object_environment()
        if not environment:
            return None

        method = MOPDispatcher.lookup_invokable(self.reflective_op(), environment)
        if method is None:
            return None
        else:
            return method.invoke(args[0], args[1:])
