from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp
from som.vmobjects.symbol import Symbol
from som.vmobjects.object import Object
from rpython.rlib import jit
from rpython.rlib.jit import we_are_jitted
from rpython.rlib.debug import make_sure_not_resized
import som.vm.universe
from rpython.rlib.jit import we_are_jitted


class MateGenericMessageNode(MateNode):

    _immutable_fields_ = ['_cache_key?', '_cache_method?', '_cache_count?']

    CACHE_SIZE = 6

    def __init__(self, som_node, source_section = None):
        MateNode.__init__(self, som_node, source_section)

        self._cache_key = [None] * MateGenericMessageNode.CACHE_SIZE
        self._cache_method = [None] * MateGenericMessageNode.CACHE_SIZE
        self._cache_count = 0

        make_sure_not_resized(self._cache_key)
        make_sure_not_resized(self._cache_method)

    def execute(self, frame):

        receiver, args = self._som_node.evaluate_rcvr_and_args(frame)
        return self.execute_evaluated(frame, receiver, args)

    def execute_evaluated(self, frame, receiver, args):

        method = None
        if not frame.meta_level():
            method = self.lookup_invokable(frame, receiver)

        if method:
            return method.invoke(receiver, args, frame)
        else:
            return self._som_node.execute_evaluated(frame, receiver, args)

    def reflective_op(self):
        return ReflectiveOp.MessageLookup

    def lookup_invokable(self, frame, receiver):
        assert frame is not None

        environment = frame.get_meta_object_environment() or receiver.get_meta_object_environment()

        # No esta definido o es Nil
        if environment is None or not isinstance(environment, Object):
            return None

        clazz = receiver.get_class(self._universe)
        cached_method = self._get_method_from_cache(environment, clazz)
        if cached_method:
            return cached_method

        method = self._lookup_node.lookup_meta_invokable(environment)
        if method is None:
            # El mate enviroment no define el methodo correspondiente a este nodo
            return None
        else:
            return self._invoke_lookup_method(frame, receiver, method, clazz)

    @jit.elidable
    def _get_method_from_cache(self, environment, clazz):
        i = 0
        while i < self._cache_count:
            if self._cache_key[i] == clazz:
                return self._cache_method[i]
            i = i + 1

    def _invoke_lookup_method(self, frame, receiver, method, clazz):

        args = [self._som_node.get_selector(), clazz]

        if self._cache_count > MateGenericMessageNode.CACHE_SIZE:
            # return clazz.lookup_invokable(args[0])
            return method.invoke_to_mate(receiver, args, frame);

        # target_method = clazz.lookup_invokable(args[0])
        target_method = method.invoke_to_mate(receiver, args, frame);

        self._cache_key[self._cache_count] = clazz
        self._cache_method[self._cache_count] = target_method
        self._cache_count = self._cache_count + 1

        return target_method

    # @jit.elidable
    # def _invoke_to_mate(self, method, receiver, args, frame):
        # return method.invoke_to_mate(receiver, args, frame);
