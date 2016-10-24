from som.interpreter.objectstorage.field_accessor_node import _UninitializedReadFieldNode, _UninitializedWriteFieldNode


class _MateUninitializedReadFieldNode(_UninitializedReadFieldNode):
    pass


class _MateUninitializedWriteFieldNode(_UninitializedWriteFieldNode):
    pass