from .contextual_node import ContextualNode
from .expression_node import ExpressionNode

from rpython.rlib import jit
from som.vmobjects.block import Block


class UninitializedReadNode(ExpressionNode):

    _immutable_fields_ = ['_var', '_context_level']

    def __init__(self, var, context_level, source_section):
        ExpressionNode.__init__(self, source_section)
        self._var           = var
        self._context_level = context_level

    def execute(self, frame):
        return self._specialize().execute(frame)

    def _specialize(self):
        return self.replace(self._var.get_initialized_read_node(
            self._context_level, self._source_section))

    def _accept(self, visitor):
        visitor.visitUninitializedReadNode(self)


class UninitializedArgumentReadNode(UninitializedReadNode):

    def _specialize(self):
        return self.replace(self._var.get_initialized_read_node(
            self._context_level, self._source_section))

    def _accept(self, visitor):
        visitor.visitUninitializedArgumentReadNode(self)


class UninitializedWriteNode(ExpressionNode):

    _immutable_fields_ = ['_var', '_context_level', '_value_expr']

    def __init__(self, var, context_level, value_expr, source_section):
        ExpressionNode.__init__(self, source_section)
        self._var           = var
        self._context_level = context_level
        self._value_expr    = value_expr

    def execute(self, frame):
        return self._specialize().execute(frame)

    def _specialize(self):
        return self.replace(self._var.get_initialized_write_node(
            self._context_level, self._value_expr, self._source_section))

    def _accept(self, visitor):
        visitor.visitUninitializedWriteNode(self)

class _NonLocalVariableNode(ContextualNode):

    _immutable_fields_ = ["_frame_idx"]

    def __init__(self, context_level, frame_idx, source_section):
        ContextualNode.__init__(self, context_level, source_section)
        assert frame_idx >= 0
        self._frame_idx = frame_idx

    def _accept(self, visitor):
        visitor.visit_NonLocalVariableNode(self)


class _NonLocalVariableReadNode(_NonLocalVariableNode):

    def execute(self, frame):
        block = self.determine_block(frame)
        return self._do_var_read(block)

    def _accept(self, visitor):
        visitor.visit_NonLocalVariableReadNode(self)


class NonLocalArgumentReadNode(_NonLocalVariableReadNode):

    def _do_var_read(self, block):
        assert isinstance(block, Block)
        return block.get_context_argument(self._frame_idx)

    def _accept(self, visitor):
        visitor.visitNonLocalArgumentReadNode(self)


class NonLocalTempReadNode(_NonLocalVariableReadNode):

    def _do_var_read(self, block):
        assert isinstance(block, Block)
        return block.get_context_temp(self._frame_idx)

    def _accept(self, visitor):
        visitor.visitNonLocalTempReadNode(self)


class NonLocalSelfReadNode(ContextualNode):

    def __init__(self, context_level, source_section):
        ContextualNode.__init__(self, context_level, source_section)

    def execute(self, frame):
        return self.determine_outer_self(frame)

    def _accept(self, visitor):
        visitor.visitNonLocalSelfReadNode(self)


class NonLocalSuperReadNode(NonLocalSelfReadNode):

    _immutable_fields_ = ["_super_class_name", "_on_class_side", "_universe"]

    def __init__(self, context_level, super_class_name, on_class_side,
                 universe, source_section = None):
        NonLocalSelfReadNode.__init__(self, context_level, source_section)
        self._super_class_name = super_class_name
        self._on_class_side    = on_class_side
        self._universe         = universe

    @jit.elidable_promote('all')
    def _get_lexical_super_class(self):
        clazz = self._universe.get_global(self._super_class_name)
        if self._on_class_side:
            clazz = clazz.get_class(self._universe)
        return clazz.get_super_class()

    def is_super_node(self):
        return True

    def get_super_class(self):
        return self._get_lexical_super_class()

    def _accept(self, visitor):
        visitor.visitNonLocalSuperReadNode(self)


class NonLocalTempWriteNode(_NonLocalVariableNode):

    _immutable_fields_ = ['_value_expr?']
    _child_nodes_      = ['_value_expr']

    def __init__(self, context_level, frame_idx, value_expr,
                 source_section = None):
        _NonLocalVariableNode.__init__(self, context_level, frame_idx,
                                       source_section)
        self._value_expr = self.adopt_child(value_expr)

    def execute(self, frame):
        value = self._value_expr.execute(frame)
        self.determine_block(frame).set_context_temp(self._frame_idx, value)
        return value

    def _accept(self, visitor):
        visitor.NonLocalTempWriteNode(self)

    def _childrenAccept(self, visitor):
        _NonLocalVariableNode._childrenAccept(self, visitor)
        self._value_expr.accept(visitor)


class _LocalVariableNode(ExpressionNode):

    _immutable_fields_ = ['_frame_idx']

    def __init__(self, frame_idx, source_section):
        ExpressionNode.__init__(self, source_section)
        assert frame_idx >= 0
        self._frame_idx = frame_idx

    def _accept(self, visitor):
        visitor.visit_LocalVariableNode(self)


class LocalArgumentReadNode(_LocalVariableNode):

    def execute(self, frame):
        return frame.get_argument(self._frame_idx)

    def _accept(self, visitor):
        visitor.visitLocalArgumentReadNode(self)


class LocalUnsharedTempReadNode(_LocalVariableNode):

    def execute(self, frame):
        return frame.get_temp(self._frame_idx)

    def _accept(self, visitor):
        visitor.visitLocalUnsharedTempReadNode(self)


class LocalSharedTempReadNode(_LocalVariableNode):

    def execute(self, frame):
        return frame.get_shared_temp(self._frame_idx)

    def _accept(self, visitor):
        visitor.visitLocalSharedTempReadNode(self)


class LocalSelfReadNode(ExpressionNode):

    def execute(self, frame):
        return frame.get_self()

    def _accept(self, visitor):
        visitor.visitLocalSelfReadNode(self)

class LocalSuperReadNode(LocalSelfReadNode):

    _immutable_fields_ = ['_super_class_name', '_on_class_side', '_universe']

    def __init__(self, super_class_name, on_class_side, universe,
                 source_section):
        LocalSelfReadNode.__init__(self, source_section)
        self._super_class_name = super_class_name
        self._on_class_side    = on_class_side
        self._universe         = universe

    def is_super_node(self):
        return True

    @jit.elidable_promote('all')
    def _get_lexical_super_class(self):
        clazz = self._universe.get_global(self._super_class_name)
        if self._on_class_side:
            clazz = clazz.get_class(self._universe)
        return clazz.get_super_class()

    def is_super_node(self):
        return True

    def get_super_class(self):
        return self._get_lexical_super_class()

    def _accept(self, visitor):
        visitor.visitLocalSuperReadNode(self)


class _LocalVariableWriteNode(_LocalVariableNode):

    _immutable_fields_ = ['_expr?']
    _child_nodes_      = ['_expr']

    def __init__(self, frame_idx, expr, source_section = None):
        _LocalVariableNode.__init__(self, frame_idx, source_section)
        self._expr = self.adopt_child(expr)

    def execute(self, frame):
        val = self._expr.execute(frame)
        self._do_write(frame, val)
        return val

    def _childrenAccept(self, visitor):
        _LocalVariableNode._childrenAccept(self, visitor)
        self._expr.accept(visitor)

    def _accept(self, visitor):
        visitor.visit_LocalVariableWriteNode(self)


class LocalSharedWriteNode(_LocalVariableWriteNode):

    def _do_write(self, frame, value):
        frame.set_shared_temp(self._frame_idx, value)

    def _accept(self, visitor):
        visitor.visitLocalSharedWriteNode(self)


class LocalUnsharedWriteNode(_LocalVariableWriteNode):

    def _do_write(self, frame, value):
        frame.set_temp(self._frame_idx, value)

    def _accept(self, visitor):
        visitor.visitLocalUnsharedWriteNode(self)
