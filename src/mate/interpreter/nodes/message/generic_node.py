from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp
from som.vmobjects.symbol import Symbol
from som.vmobjects.object import Object
from rpython.rlib import jit
from rpython.rlib.jit import we_are_jitted
from rpython.rlib.debug import make_sure_not_resized
import som.vm.universe


class MateGenericMessageNode(MateNode):

    CACHE_SIZE = 10

    def __init__(self, som_node, source_section = None):
        MateNode.__init__(self, som_node, source_section)

        self._cache_key = [None] * MateGenericMessageNode.CACHE_SIZE
        self._cache_method = [None] * MateGenericMessageNode.CACHE_SIZE
        self._cache_count = 0

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

        method = self._lookup_node.lookup_meta_invokable(environment)

        if method is None:
            # El mate enviroment no define el methodo correspondiente a este nodo
            return None

        args = [self._som_node.get_selector(), receiver.get_class(som.vm.universe.get_current())]

        if self._cache_count > MateGenericMessageNode.CACHE_SIZE:
            return self._invoke_to_mate(method, receiver, args, frame)

        cache_key = str(args[1])+ '>>' + str(args[0])
        for i in xrange(0, self._cache_count):
            if self._cache_key[i] == cache_key:
                return self._cache_method[i]

        target_method = self._invoke_to_mate(method, receiver, args, frame)

        self._cache_key[self._cache_count] = cache_key
        self._cache_method[self._cache_count] = target_method
        self._cache_count = self._cache_count + 1

        return target_method

    # @jit.elidable
    def _invoke_to_mate(self, method, receiver, args, frame):
        return method.invoke_to_mate(receiver, args, frame);
