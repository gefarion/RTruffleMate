from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp


class MateReturnNonLocalNode(MateNode):

    def __init__(self, som_node, source_section = None):
        MateNode.__init__(self, som_node, source_section)

    def execute(self, frame):

        receiver = frame.get_self()
        result = self._som_node.get_expr().execute(frame)
        value = self.do_mate_semantics(frame, receiver, [result])

        if value is None:
            return self._som_node.execute_prevaluated(frame, [result])
        else:
            return value

    def reflectiveOp(self):
        return ReflectiveOp.ExecutorReturn


class MateCatchNonLocalReturnNode(MateNode):

    def reflectiveOp(self):
        return ReflectiveOp.ExecutorReturn
