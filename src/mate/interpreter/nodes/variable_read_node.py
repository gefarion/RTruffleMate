from som.interpreter.nodes.variable_read_node import UninitializedReadNode
from som.interpreter.nodes.variable_read_node import UninitializedArgumentReadNode
from som.interpreter.nodes.variable_read_node import UninitializedWriteNode
from som.interpreter.nodes.variable_read_node import NonLocalArgumentReadNode
from som.interpreter.nodes.variable_read_node import NonLocalTempReadNode
from som.interpreter.nodes.variable_read_node import NonLocalSelfReadNode
from som.interpreter.nodes.variable_read_node import NonLocalSuperReadNode
from som.interpreter.nodes.variable_read_node import NonLocalTempWriteNode
from som.interpreter.nodes.variable_read_node import LocalArgumentReadNode
from som.interpreter.nodes.variable_read_node import LocalUnsharedTempReadNode
from som.interpreter.nodes.variable_read_node import LocalSharedTempReadNode
from som.interpreter.nodes.variable_read_node import LocalSelfReadNode
from som.interpreter.nodes.variable_read_node import LocalSuperReadNode
from som.interpreter.nodes.variable_read_node import LocalSharedWriteNode
from som.interpreter.nodes.variable_read_node import LocalUnsharedWriteNode


class MateUninitializedReadNode(UninitializedReadNode):

    @classmethod
    def mateify(cls, node):
        return cls(node._var, node._context_level, node._source_section)


class MateUninitializedArgumentReadNode(UninitializedArgumentReadNode):
    pass


class MateUninitializedWriteNode(UninitializedWriteNode):

    @classmethod
    def mateify(cls, node):
        return cls(node._var, node._context_level, node._value_expr, node._source_section)


class MateNonLocalArgumentReadNode(NonLocalArgumentReadNode):
    pass


class MateNonLocalTempReadNode(NonLocalTempReadNode):
    pass


class MateNonLocalSelfReadNode(NonLocalSelfReadNode):
    pass


class MateNonLocalSuperReadNode(NonLocalSuperReadNode):
    pass


class MateNonLocalTempWriteNode(NonLocalTempWriteNode):
    pass


class MateLocalArgumentReadNode(LocalArgumentReadNode):

    @classmethod
    def mateify(cls, node):
        return cls(node._frame_idx, node._source_section)


class MateLocalUnsharedTempReadNode(LocalUnsharedTempReadNode):
    pass


class MateLocalSharedTempReadNode(LocalSharedTempReadNode):
    pass


class MateLocalSelfReadNode(LocalSelfReadNode):

    @classmethod
    def mateify(cls, node):
        return cls(node._source_section)


class MateLocalSuperReadNode(LocalSuperReadNode):
    pass


class MateLocalSharedWriteNode(LocalSharedWriteNode):
    pass


class MateLocalUnsharedWriteNode(LocalUnsharedWriteNode):
    pass