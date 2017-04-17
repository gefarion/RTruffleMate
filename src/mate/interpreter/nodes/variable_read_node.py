from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp

class MateUninitializedReadNode(MateNode):

    def reflectiveOp(self):
        return ReflectiveOp.ExecutorReadLocal
    

class MateUninitializedArgumentReadNode(MateNode):

    def execute(self, frame):

        receiver = self._som_node.receiver(frame)
        value = self.do_mate_semantics(frame, receiver, [Integer(self._som_node.frame_idx()), Frame])

        if value is None:
            return self._som_node.execute_evaluated(frame, receiver, None)
        else:
            return value

    def reflectiveOp(self):
        return ReflectiveOp.ExecutorLocalArg


class MateUninitializedWriteNode(MateNode):

    def reflectiveOp(self):
        return ReflectiveOp.ExecutorWriteLocal

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