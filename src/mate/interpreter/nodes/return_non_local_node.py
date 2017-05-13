from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp


class MateReturnNonLocalNode(MateNode):

    def reflective_op(self):
        return ReflectiveOp.ExecutorReturn

class MateCatchNonLocalReturnNode(MateNode):

    def reflective_op(self):
        return ReflectiveOp.ExecutorReturn