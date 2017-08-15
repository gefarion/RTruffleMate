from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp
from som.vmobjects.symbol import Symbol
from som.vmobjects.object import Object
from mate.interpreter.mop import MOPDispatcher

class MateGenericMessageNode(MateNode):

    def execute(self, frame):

        receiver, args = self._som_node.evaluate_rcvr_and_args(frame)
        return self.execute_evaluated(frame, receiver, args)

    def execute_evaluated(self, frame, receiver, args):

        method = None
        if not frame.meta_level():
            method = self.lookup_invokable(frame, receiver)

        if method:
            # ejecutar el ih para activation
            return method.invoke(receiver, args, False)
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

        args = [self._som_node.get_selector(), receiver.get_class(self._som_node.get_universe())]

        return  method.invoke(receiver, args, True)
