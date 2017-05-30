from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp

class MateReturnLocalNode(MateNode):

    def get_meta_args(self, frame):
        return [self._som_node.get_expr().execute(frame)]

    def reflective_op(self):
        return ReflectiveOp.ExecutorReturn

class MateReturnNonLocalNode(MateNode):

    def reflective_op(self):
        return ReflectiveOp.ExecutorReturn
