from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp

class MateUninitializedReadNode(MateNode):

    def mateOn:
        return True

    def reflectiveOp(self):
        return ReflectiveOp.ExecutorReadLocal
    

class MateUninitializedArgumentReadNode(MateNode):

    def mateOn:
        return True

    def reflectiveOp(self):
        return ReflectiveOp.ExecutorLocalArg


class MateUninitializedWriteNode(MateNode):

    def mateOn:
        return True

    def reflectiveOp(self):
        return ReflectiveOp.ExecutorWriteLocal

class MateNonLocalArgumentReadNode(MateNode):
    
    def reflectiveOp(self):
        return ReflectiveOp.ExecutorNonLocalArg


class MateNonLocalTempReadNode(MateNode):

    def mateOn:
        return True
    
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