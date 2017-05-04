from .expression_node import ExpressionNode

from rpython.rlib.jit import unroll_safe


class SequenceNode(ExpressionNode):

    _immutable_fields_ = ['_exprs?[*]']
    _child_nodes_      = ['_exprs[*]']

    def __init__(self, expressions, source_section):
        ExpressionNode.__init__(self, source_section)
        self._exprs = self.adopt_children(expressions)

    def execute(self, frame):
        self._execute_all_but_last(frame)
        return self._exprs[-1].execute(frame)

    @unroll_safe
    def _execute_all_but_last(self, frame):
        for i in range(0, len(self._exprs) - 1):
            self._exprs[i].execute(frame)

    def _accept(self, visitor):
        visitor.visit_SequenceNode(self)

    def _children_accept(self, visitor):
        ExpressionNode._children_accept(self, visitor)
        for child in self._exprs:
            child.accept(visitor)
