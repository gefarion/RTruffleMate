from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp
from mate.interpreter.nodes.message.generic_node import MateGenericMessageNode
from som.interpreter.nodes.message.generic_node import GenericMessageNode

class MateUninitializedMessageNode(MateNode):

    def _mate_specialize(self, frame, rcvr, args):

        if (isinstance(self._som_node.message_specialize(frame, rcvr, args), GenericMessageNode)):
            return self.replace(MateGenericMessageNode(self._som_node))
        else:
            return self.replace(self._som_node)

    def execute(self, frame):

        rcvr, args = self._som_node.evaluate_rcvr_and_args(frame)
        return self._mate_specialize(frame, rcvr, args).execute_evaluated(frame, rcvr, args)

    def reflective_op(self):
        return ReflectiveOp.MessageLookup