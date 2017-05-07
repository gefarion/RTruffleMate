from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp


class MateReturnNonLocalNode(MateNode):

    def __init__(self, som_node, source_section = None):
        MateNode.__init__(self, som_node, source_section)

    def reflectiveOp(self):
        return ReflectiveOp.ExecutorReturn


class MateCatchNonLocalReturnNode(MateNode):

    def reflectiveOp(self):
        return ReflectiveOp.ExecutorReturn
