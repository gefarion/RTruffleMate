from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp


class MateReturnLocalNode(MateNode):

    def reflective_op(self):
        return ReflectiveOp.ExecutorReturn

class MateReturnNonLocalNode(MateNode):

    def reflective_op(self):
        return ReflectiveOp.ExecutorReturn
