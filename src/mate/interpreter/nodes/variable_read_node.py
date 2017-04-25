from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp
from som.vmobjects.integer import Integer
from som.vmobjects.string import String
from som.vmobjects.context import Context

class MateUninitializedReadNode(MateNode):

    _immutable_fields_ = ["_som_node?", "_var"]

    def __init__(self, som_node, source_section = None):
        MateNode.__init__(self, som_node, source_section)
        self._var_name = som_node.get_var().get_name()

    def execute(self, frame):

        receiver = frame.get_self()
        value = self.do_mate_semantics(frame, receiver, [String(self._var_name), Context(frame)])

        if value is None:
            return self._som_node.execute_prevaluated(frame, [])
        else:
            return value

    def reflectiveOp(self):
        return ReflectiveOp.ExecutorReadLocal

class MateUninitializedWriteNode(MateNode):

    _immutable_fields_ = ["_som_node?", "_var"]

    def __init__(self, som_node, source_section = None):
        MateNode.__init__(self, som_node, source_section)
        self._var_name = som_node.get_var().get_name()

    def execute(self, frame):

        receiver = frame.get_self()
        value_expr = self._som_node.get_value_expr().execute(frame)

        value = self.do_mate_semantics(frame, receiver, [String(self._var_name), Context(frame), value_expr])

        if value is None:
            return self._som_node.execute_prevaluated(frame, [value_expr])
        else:
            return value

    def reflectiveOp(self):
        return ReflectiveOp.ExecutorWriteLocal

class MateUninitializedArgumentReadNode(MateNode):

    def execute(self, frame):

        receiver = frame.get_self()
        value = self.do_mate_semantics(frame, receiver, [Integer(self._som_node.frame_idx()), Context(frame)])

        if value is None:
            return self._som_node.execute_prevaluated(frame, [])
        else:
            return value

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