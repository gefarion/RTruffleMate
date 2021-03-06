from rpython.rlib import jit

from ..expression_node import ExpressionNode
from som.vm.globals import nilObject, falseObject, trueObject

from ....vmobjects.block  import Block
from ....vmobjects.method import Method


class AbstractWhileMessageNode(ExpressionNode):

    _immutable_fields_ = ['_predicate_bool', '_rcvr_expr?', '_body_expr?',
                          '_universe']
    _child_nodes_      = ['_rcvr_expr', '_body_expr']

    def __init__(self, rcvr_expr, body_expr, predicate_bool_obj, universe,
                 source_section):
        ExpressionNode.__init__(self, source_section)
        self._predicate_bool = predicate_bool_obj
        self._rcvr_expr      = self.adopt_child(rcvr_expr)
        self._body_expr      = self.adopt_child(body_expr)
        self._universe       = universe

    def get_universe(self):
        return self._universe

    def get_selector(self):
        if self._predicate_bool is trueObject:
            return self._universe.symbol_for("whileTrue:")
        else:
            return self._universe.symbol_for("whileFalse:")

    def evaluate_rcvr_and_args(self, frame):
        rcvr_value = self._rcvr_expr.execute(frame)
        body_block = self._body_expr.execute(frame)

        return rcvr_value, [body_block]

    def execute(self, frame):
        rcvr_value = self._rcvr_expr.execute(frame)
        body_block = self._body_expr.execute(frame)

        self._do_while(rcvr_value, body_block, frame.meta_level())
        return nilObject

# def get_printable_location_while_value(body_method, node):
#     assert isinstance(body_method, Method)
#     return "while_value: %s" % body_method.merge_point_string()
#
# while_value_driver = jit.JitDriver(
#     greens=['body_method', 'node'], reds='auto',
#     get_printable_location = get_printable_location_while_value)
#
#
# class WhileWithValueReceiver(AbstractWhileMessageNode):
#
#     def execute_evaluated(self, frame, rcvr_value, body_block):
#         if rcvr_value is not self._predicate_bool:
#             return nilObject
#         body_method = body_block.get_method()
#
#         while True:
#             while_value_driver.jit_merge_point(body_method = body_method,
#                                                node        = self)
#             body_method.invoke(body_block, None, meta_level)


def get_printable_location_while(body_method, condition_method, while_type):
    assert isinstance(condition_method, Method)
    assert isinstance(body_method, Method)

    return "%s while %s: %s" % (condition_method.merge_point_string(),
                                while_type,
                                body_method.merge_point_string())


while_driver = jit.JitDriver(
    greens=['body_method', 'condition_method', 'node'], reds='auto',
    is_recursive=True,
    get_printable_location = get_printable_location_while)


class WhileMessageNode(AbstractWhileMessageNode):

    def execute_evaluated(self, frame, rcvr, args):
        self._do_while(rcvr, args[0], frame.meta_level())
        return nilObject

    def _do_while(self, rcvr_block, body_block, meta_level):
        condition_method = rcvr_block.get_method()
        body_method      = body_block.get_method()

        if rcvr_block.is_same_context(body_block):
            rcvr_block = body_block

        while True:
            while_driver.jit_merge_point(body_method     = body_method,
                                         condition_method= condition_method,
                                         node            = self)

            # STEFAN: looks stupid but might help the jit
            if rcvr_block is body_block:
                rcvr_block = body_block

            condition_value = condition_method.invoke(rcvr_block, [], meta_level)
            if condition_value is not self._predicate_bool:
                break
            body_method.invoke(body_block, [], meta_level)

    @staticmethod
    def can_specialize(selector, rcvr, args, node):
        sel = selector.get_string()
        return isinstance(args[0], Block) and (sel == "whileTrue:" or
                                               sel == "whileFalse:")

    @staticmethod
    def specialize_node(selector, rcvr, args, node):
        sel = selector.get_string()
        if sel == "whileTrue:":
            return node.replace(
                WhileMessageNode(node._rcvr_expr, node._arg_exprs[0],
                                 trueObject, node._universe,
                                 node._source_section))
        else:
            assert sel == "whileFalse:"
            return node.replace(
                WhileMessageNode(node._rcvr_expr, node._arg_exprs[0],
                                 falseObject, node._universe,
                                 node._source_section))
