from mate.interpreter.nodes.mate_node import MateNode

class MateUninitializedReadNode(MateNode):
    pass


class MateUninitializedArgumentReadNode(MateNode):
    pass


class MateUninitializedWriteNode(MateNode):
    pass


class MateNonLocalArgumentReadNode(MateNode):
    pass


class MateNonLocalTempReadNode(MateNode):
    pass


class MateNonLocalSelfReadNode(MateNode):
    pass


class MateNonLocalSuperReadNode(MateNode):
    pass


class MateNonLocalTempWriteNode(MateNode):
    pass


class MateLocalArgumentReadNode(MateNode):
    pass


class MateLocalUnsharedTempReadNode(MateNode):
    pass


class MateLocalSharedTempReadNode(MateNode):
    pass


class MateLocalSelfReadNode(MateNode):
    pass


class MateLocalSuperReadNode(MateNode):
    pass


class MateLocalSharedWriteNode(MateNode):
    pass


class MateLocalUnsharedWriteNode(MateNode):
    pass