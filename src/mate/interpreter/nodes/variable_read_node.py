from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp

class MateUninitializedReadNode(MateNode):

    def __init__(self, som_node, source_section = None):
        MateNode.__init__(self, som_node, source_section)

    def reflective_op(self):
        return ReflectiveOp.ExecutorReadLocal

class MateUninitializedWriteNode(MateNode):

    def __init__(self, som_node, source_section = None):
        MateNode.__init__(self, som_node, source_section)

    def reflective_op(self):
        return ReflectiveOp.ExecutorWriteLocal

class MateUninitializedArgumentReadNode(MateNode):

    def __init__(self, som_node, source_section = None):
        MateNode.__init__(self, som_node, source_section)

    def reflective_op(self):
        return ReflectiveOp.ExecutorLocalArg

class MateNonLocalArgumentReadNode(MateNode):
    
    def reflective_op(self):
        return ReflectiveOp.ExecutorNonLocalArg


class MateNonLocalTempReadNode(MateNode):
    
    def reflective_op(self):
        return ReflectiveOp.ExecutorReadNonLocalTemp


class MateNonLocalSelfReadNode(MateNode):

    def reflective_op(self):
        return ReflectiveOp.ExecutorNonLocalSelf


class MateNonLocalSuperReadNode(MateNode):
    
    def reflective_op(self):
        return ReflectiveOp.ExecutorNonLocalSuperArg


class MateNonLocalTempWriteNode(MateNode):

    def reflective_op(self):
        return ReflectiveOp.ExecutorWriteNonLocalTemp


class MateLocalArgumentReadNode(MateNode):

    def reflective_op(self):
        return ReflectiveOp.ExecutorLocalArg


class MateLocalUnsharedTempReadNode(MateNode):
    # TODO: Buscar que significa
    pass


class MateLocalSharedTempReadNode(MateNode):
    # TODO: Buscar que significa
    pass


class MateLocalSelfReadNode(MateNode):

    def reflective_op(self):
        return ReflectiveOp.ExecutorLocalSelf


class MateLocalSuperReadNode(MateNode):

    def reflective_op(self):
        return ReflectiveOp.ExecutorLocalSuper



class MateLocalSharedWriteNode(MateNode):
    # TODO: Investigar para que es
    pass


class MateLocalUnsharedWriteNode(MateNode):
    # TODO: Investigar para que es
    pass