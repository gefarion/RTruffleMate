from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp
from som.vmobjects.symbol import Symbol
from som.vmobjects.object import Object
from mate.interpreter.mop import MOPDispatcher

class MateGenericMessageNode(MateNode):

    def execute(self, frame):

        receiver, args = self._som_node._evaluate_rcvr_and_args(frame)
        return self.execute_evaluated(frame, receiver, args)

    def execute_evaluated(self, frame, receiver, args):

        method = self.lookup_invokable(frame, receiver)
        if method:
            return method.invoke(receiver, args)
        else:
            return self._som_node.execute_evaluated(frame, receiver, args)

    def reflective_op(self):
        return ReflectiveOp.MessageLookup


    def lookup_invokable(self, frame, receiver):
        assert frame is not None

        receiver = frame.get_self()
        environment = frame.get_meta_object_environment() or receiver.get_meta_object_environment()

        # No esta definido o es Nil
        if environment is None or not isinstance(environment, Object):
            return None

        method = MOPDispatcher.lookup_invokable(self.reflective_op(), environment)
        if method is None:
            # El mate enviroment no define el methodo correspondiente a este nodo
            return None

        args = [self._som_node.get_selector(), receiver.get_class(self._som_node.get_universe())]

        # Tengo que desactivar mate para evitar recursion infinita, ver como implementar una solucion con niveles de contexto
        receiver.set_meta_object_environment(None)
        res = method.invoke(receiver, args)
        receiver.set_meta_object_environment(environment)

        return res
