from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp
from som.vmobjects.integer import Integer
from som.vmobjects.string import String
from som.vmobjects.context import Context

class MateUninitializedReadNode(MateNode):

    def __init__(self, som_node, source_section = None):
        MateNode.__init__(self, som_node, source_section)

    def reflectiveOp(self):
        return ReflectiveOp.ExecutorReadLocal

class MateUninitializedWriteNode(MateNode):

    def __init__(self, som_node, source_section = None):
        MateNode.__init__(self, som_node, source_section)

    def reflectiveOp(self):
        return ReflectiveOp.ExecutorWriteLocal

class MateUninitializedArgumentReadNode(MateNode):

    def __init__(self, som_node, source_section = None):
        MateNode.__init__(self, som_node, source_section)

    def reflectiveOp(self):
        return ReflectiveOp.ExecutorLocalArg

class MateNonLocalArgumentReadNode(MateNode):
    
    def reflectiveOp(self):
        return ReflectiveOp.ExecutorNonLocalArg


class MateNonLocalTempReadNode(MateNode):
    
    def reflectiveOp(self):
        return ReflectiveOp.ExecutorReadNonLocalTemp


class MateNonLocalSelfReadNode(MateNode):

    def reflectiveOp(self):
        return ReflectiveOp.ExecutorNonLocalSelf


class MateNonLocalSuperReadNode(MateNode):
    
    def reflectiveOp(self):
        return ReflectiveOp.ExecutorNonLocalSuperArg


class MateNonLocalTempWriteNode(MateNode):

    def reflectiveOp(self):
        return ReflectiveOp.ExecutorWriteNonLocalTemp


class MateLocalArgumentReadNode(MateNode):

    def reflectiveOp(self):
        return ReflectiveOp.ExecutorLocalArg


class MateLocalUnsharedTempReadNode(MateNode):
    # TODO: Buscar que significa
    pass


class MateLocalSharedTempReadNode(MateNode):
    # TODO: Buscar que significa
    pass


class MateLocalSelfReadNode(MateNode):

    def reflectiveOp(self):
        return ReflectiveOp.ExecutorLocalSelf


class MateLocalSuperReadNode(MateNode):

    def reflectiveOp(self):
        return ReflectiveOp.ExecutorLocalSuper



class MateLocalSharedWriteNode(MateNode):
    # TODO: Investigar para que es
    pass


class MateLocalUnsharedWriteNode(MateNode):
    # TODO: Investigar para que es
    pass