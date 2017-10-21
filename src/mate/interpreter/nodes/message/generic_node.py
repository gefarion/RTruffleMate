from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp
from som.vmobjects.symbol import Symbol
from som.vmobjects.object import Object
from rpython.rlib import jit
from rpython.rlib.jit import we_are_jitted
from rpython.rlib.debug import make_sure_not_resized
import som.vm.universe
from mate.interpreter.nodes.dispatch import UninitializedMateDispatchNode

class MateGenericMessageNode(MateNode):

    _immutable_fields_ = ['_mate_dispatch?']
    _child_nodes_ = ['_mate_dispatch']

    def __init__(self, som_node, source_section = None):
        MateNode.__init__(self, som_node, source_section)
        self._mate_dispatch = self.adopt_child(UninitializedMateDispatchNode(self._som_node.get_selector(), som.vm.universe.get_current()))

    def replace_mate_dispatch_list_head(self, node):
        self._mate_dispatch.replace(node)

    def execute(self, frame):

        receiver, args = self._som_node.evaluate_rcvr_and_args(frame)
        return self.execute_evaluated(frame, receiver, args)

    def execute_evaluated(self, frame, receiver, args):

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

    ################

    # def lookup_invokable(self, frame, receiver):
    #     assert frame is not None


    #     else:
    #         return self._invoke_lookup_method(frame, receiver, method, clazz)

    # @jit.elidable
    # def _get_method_from_cache(self, environment, clazz):
    #     i = 0
    #     while i < self._cache_count:
    #         if self._cache_key[i] == clazz:
    #             return self._cache_method[i]
    #         i = i + 1

    # def _invoke_lookup_method(self, frame, receiver, method, clazz):

    #     args = [self._som_node.get_selector(), clazz]

    #     if self._cache_count > MateGenericMessageNode.CACHE_SIZE:
    #         # return clazz.lookup_invokable(args[0])
    #         return method.invoke_to_mate(receiver, args, frame);

    #     # target_method = clazz.lookup_invokable(args[0])
    #     target_method = method.invoke_to_mate(receiver, args, frame);

    #     self._cache_key[self._cache_count] = clazz
    #     self._cache_method[self._cache_count] = target_method
    #     self._cache_count = self._cache_count + 1

    #     return target_method

    # @jit.elidable
    # def _invoke_to_mate(self, method, receiver, args, frame):
        # return method.invoke_to_mate(receiver, args, frame);
