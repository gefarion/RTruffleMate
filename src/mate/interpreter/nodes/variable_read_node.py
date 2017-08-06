from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp
from som.vmobjects.integer import Integer
from som.vmobjects.string import String
from som.vmobjects.context import Context

class MateUninitializedReadNode(MateNode):

    def get_meta_args(self, frame):
        self._som_node.specializeReadNode()
        return self.replace(MateReadNode(self._som_node)).get_meta_args(frame)

    def reflective_op(self):
        return ReflectiveOp.ExecutorReadLocal

class MateReadNode(MateNode):

    def get_meta_args(self, frame):
        return [Integer(self._som_node.frame_idx() + 1), Context(frame)]

    def reflective_op(self):
        return ReflectiveOp.ExecutorReadLocal

class MateUninitializedWriteNode(MateNode):

    def get_meta_args(self, frame):
        self._som_node.specializeWriteNode()
        return self.replace(MateWriteNode(self._som_node)).get_meta_args(frame)

    def reflective_op(self):
        return ReflectiveOp.ExecutorWriteLocal

class MateWriteNode(MateNode):

    def get_meta_args(self, frame):
        value = self._som_node.get_expr().execute(frame)
        return [Integer(self._som_node.frame_idx() + 1), Context(frame), value]

    def reflective_op(self):
        return ReflectiveOp.ExecutorWriteLocal

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

    def get_meta_args(self, frame):
        return [Integer(self._som_node.frame_idx() + 1), Context(frame)]

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