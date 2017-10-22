from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp
from som.vmobjects.symbol import Symbol
from som.vmobjects.object import Object
from rpython.rlib import jit
from rpython.rlib.jit import we_are_jitted
from rpython.rlib.debug import make_sure_not_resized
import som.vm.universe
from mate.interpreter.nodes.dispatch import UninitializedMateDispatchNode
from som.interpreter.nodes.message.abstract_node import AbstractMessageNode

class MateGenericMessageNode(MateNode):

    _immutable_fields_ = ['_mate_dispatch?', '_universe']
    _child_nodes_ = ['_mate_dispatch']

    def __init__(self, som_node, source_section = None):

        MateNode.__init__(self, som_node, source_section)
        self._mate_dispatch = self.adopt_child(UninitializedMateDispatchNode(self._som_node.get_selector(), som.vm.universe.get_current()))
        self._universe = som.vm.universe.get_current()

    def replace_mate_dispatch_list_head(self, node):
        self._mate_dispatch.replace(node)

    def execute(self, frame):

        receiver, args = self._som_node.evaluate_rcvr_and_args(frame)
        return self.execute_evaluated(frame, receiver, args)

    def execute_evaluated(self, frame, receiver, args):

        # if not isinstance(self._som_node, AbstractMessageNode):
        #     return self.replace(self._som_node).execute_evaluated(frame, receiver, args)
            # No proceso los nodos especializados (if, while, etc)
            # return self._som_node

        value = None
        if not frame.meta_level():
            value = self._do_mate_dispatch(frame, receiver, args)

        if value:
            return value
        else:
            return self._som_node.execute_evaluated(frame, receiver, args)

    def reflective_op(self):
        return ReflectiveOp.MessageLookup

    def _do_mate_dispatch(self, frame, receiver, args):

        environment = frame.get_meta_object_environment() or receiver.get_meta_object_environment()

        # No esta definido o es Nil
        if environment is None or not isinstance(environment, Object):
            return None

        lookup_method = self._lookup_node.lookup_meta_invokable(environment)
        if lookup_method is None:
            # El mate enviroment no define el methodo correspondiente a este nodo
            return None

        # if we_are_jitted():
            # return self._direct_mate_dispatch(receiver, args, frame, lookup_method)
        # else:
        return self._mate_dispatch.execute_mate_dispatch(receiver, args, frame, lookup_method)

    def _direct_mate_dispatch(self, rcvr, args, frame, lookup_method):
        method = lookup_method.invoke_to_mate(rcvr, [self._som_node.get_selector(), rcvr.get_class(self._universe)], frame)
        if method is None:
            return None
        else:
            return method.invoke(rcvr, args, frame)