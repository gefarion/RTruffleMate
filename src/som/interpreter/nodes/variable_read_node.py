from .contextual_node import ContextualNode
from .expression_node import ExpressionNode
from som.vmobjects.integer import Integer
from som.vmobjects.string import String
from som.vmobjects.context import Context

from rpython.rlib import jit
from som.vmobjects.block import Block


class UninitializedReadNode(ExpressionNode):

    _immutable_fields_ = ['_var', '_context_level']

    def __init__(self, var, context_level, source_section):
        ExpressionNode.__init__(self, source_section)
        self._var           = var
        self._context_level = context_level

    def get_var(self):
        return self._var

    def  get_execute_args(self, frame):
        return self._specialize().get_execute_args(frame)

    def execute(self, frame):
        return self._specialize().execute(frame)

    def _specialize(self):
        return self.replace(self._var.get_initialized_read_node(
            self._context_level, self._source_section))

    def _accept(self, visitor):
        visitor.visit_UninitializedReadNode(self)


class UninitializedArgumentReadNode(UninitializedReadNode):

    def  get_execute_args(self, frame):
        return self._specialize().get_execute_args(frame)

    def _specialize(self):
        return self.replace(self._var.get_initialized_read_node(
            self._context_level, self._source_section))

    def _accept(self, visitor):
        visitor.visit_UninitializedArgumentReadNode(self)


class UninitializedWriteNode(ExpressionNode):

    _immutable_fields_ = ['_var', '_context_level', '_value_expr']
    _child_nodes_ = ['_value_expr']

    def __init__(self, var, context_level, value_expr, source_section):
        ExpressionNode.__init__(self, source_section)
        self._var           = var
        self._context_level = context_level
        self._value_expr    = self.adopt_child(value_expr)

    def get_var(self):
        return self._var

    def  get_execute_args(self, frame):
        return self._specialize().get_execute_args(frame)

    def execute(self, frame):
        return self._specialize().execute(frame)

    def _specialize(self):
        return self.replace(self._var.get_initialized_write_node(
            self._context_level, self._value_expr, self._source_section))

    def _accept(self, visitor):
        visitor.visit_UninitializedWriteNode(self)

    def _children_accept(self, visitor):
        ExpressionNode._children_accept(self, visitor)
        self._value_expr.accept(visitor)

class _NonLocalVariableNode(ContextualNode):

    _immutable_fields_ = ["_frame_idx", "var"]

    def __init__(self, context_level, frame_idx, source_section, var):
        ContextualNode.__init__(self, context_level, source_section)
        assert frame_idx >= 0
        self._frame_idx = frame_idx
        self._var = var

    def get_var(self):
        return self._var

    def frame_idx(self):
        return self._frame_idx

    def _accept(self, visitor):
        visitor.visit_NonLocalVariableNode(self)


class _NonLocalVariableReadNode(_NonLocalVariableNode):

    def get_execute_args(self, frame):
        return [String(self._var.get_name()), Context(frame)]

    def execute_prevaluated(self, frame, args):
        return self.execute(frame)

    def execute(self, frame):
        block = self.determine_block(frame)
        return self._do_var_read(block)

    def _accept(self, visitor):
        visitor.visit_NonLocalVariableReadNode(self)


class NonLocalArgumentReadNode(_NonLocalVariableReadNode):

    def execute_prevaluated(self, frame, args):
        return self.execute(frame)

    def get_execute_args(self, frame):
        return [Integer(self._frame_idx + 1), Context(frame)]

    def _do_var_read(self, block):
        assert isinstance(block, Block)
        return block.get_context_argument(self._frame_idx)

    def _accept(self, visitor):
        visitor.visit_NonLocalArgumentReadNode(self)


class NonLocalTempReadNode(_NonLocalVariableReadNode):

    def _do_var_read(self, block):
        assert isinstance(block, Block)
        return block.get_context_temp(self._frame_idx)

    def _accept(self, visitor):
        visitor.visit_NonLocalTempReadNode(self)


class NonLocalSelfReadNode(ContextualNode):

    def __init__(self, context_level, source_section):
        ContextualNode.__init__(self, context_level, source_section)

    def execute(self, frame):
        return self.determine_outer_self(frame)

    def _accept(self, visitor):
        visitor.visit_NonLocalSelfReadNode(self)


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
        visitor.visit_NonLocalSuperReadNode(self)


class NonLocalTempWriteNode(_NonLocalVariableNode):

    _immutable_fields_ = ['_value_expr?']
    _child_nodes_      = ['_value_expr']

    def __init__(self, context_level, frame_idx, value_expr,
                 source_section, var):
        _NonLocalVariableNode.__init__(self, context_level, frame_idx,
                                       source_section, var)
        self._value_expr = self.adopt_child(value_expr)

    def get_execute_args(self, frame):
        value = self._value_expr.execute(frame)
        return [String(self._var.get_name()), Context(frame), value]

    def execute_prevaluated(self, frame, args):
        value = args[3]
        self.determine_block(frame).set_context_temp(self._frame_idx, value)
        return value

    def execute(self, frame):
        value = self._value_expr.execute(frame)
        self.determine_block(frame).set_context_temp(self._frame_idx, value)
        return value

    def _accept(self, visitor):
        visitor.visit_NonLocalTempWriteNode(self)

    def _children_accept(self, visitor):
        _NonLocalVariableNode._children_accept(self, visitor)
        self._value_expr.accept(visitor)


class _LocalVariableNode(ExpressionNode):

    _immutable_fields_ = ['_frame_idx']

    def __init__(self, frame_idx, source_section, var):
        ExpressionNode.__init__(self, source_section)
        assert frame_idx >= 0
        self._frame_idx = frame_idx
        self._var = var

    def _accept(self, visitor):
        visitor.visit_LocalVariableNode(self)


class LocalArgumentReadNode(_LocalVariableNode):

    def execute(self, frame):
        return frame.get_argument(self._frame_idx)

    def get_execute_args(self, frame):
        return [Integer(self._frame_idx + 1), Context(frame)]

    def execute_prevaluated(self, frame, args):
        return self.execute(frame)

    def _accept(self, visitor):
        visitor.visit_LocalArgumentReadNode(self)


class LocalUnsharedTempReadNode(_LocalVariableNode):

    def execute(self, frame):
        return frame.get_temp(self._frame_idx)

    def execute_prevaluated(self, frame, args):
        return self.execute(frame)

    def get_execute_args(self, frame):
        return [String(self._var.get_name()), Context(frame)]

    def _accept(self, visitor):
        visitor.visit_LocalUnsharedTempReadNode(self)


class LocalSharedTempReadNode(_LocalVariableNode):

    def execute(self, frame):
        return frame.get_shared_temp(self._frame_idx)

    def execute_prevaluated(self, frame, args):
        return self.execute(frame)

    def get_execute_args(self, frame):
        return [String(self._var.get_name()), Context(frame)]

    def _accept(self, visitor):
        visitor.visit_LocalSharedTempReadNode(self)


class LocalSelfReadNode(ExpressionNode):

    def execute(self, frame):
        return frame.get_self()

    def _accept(self, visitor):
        visitor.visit_LocalSelfReadNode(self)

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
        visitor.visit_LocalSuperReadNode(self)


class _LocalVariableWriteNode(_LocalVariableNode):

    _immutable_fields_ = ['_expr?']
    _child_nodes_      = ['_expr']

    def __init__(self, frame_idx, expr, source_section, var):
        _LocalVariableNode.__init__(self, frame_idx, source_section, var)
        self._expr = self.adopt_child(expr)

    def get_execute_args(self, frame):
        return [String(self._var.get_name()), Context(frame), self._expr.execute(frame)]

    def execute_prevaluated(self, frame, args):
        val = args[2]
        self._do_write(frame, val)
        return val

    def execute(self, frame):
        val = self._expr.execute(frame)
        self._do_write(frame, val)
        return val

    def get_expr(self):
        return self._expr

    def _children_accept(self, visitor):
        _LocalVariableNode._children_accept(self, visitor)
        self._expr.accept(visitor)

    def _accept(self, visitor):
        visitor.visit_LocalVariableWriteNode(self)


class LocalSharedWriteNode(_LocalVariableWriteNode):

    def _do_write(self, frame, value):
        frame.set_shared_temp(self._frame_idx, value)

    def _accept(self, visitor):
        visitor.visit_LocalSharedWriteNode(self)


class LocalUnsharedWriteNode(_LocalVariableWriteNode):

    def _do_write(self, frame, value):
        frame.set_temp(self._frame_idx, value)

    def _accept(self, visitor):
        visitor.visit_LocalUnsharedWriteNode(self)
