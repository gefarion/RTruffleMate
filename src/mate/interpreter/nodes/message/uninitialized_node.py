from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp


class MateUninitializedMessageNode(MateNode):

    def _specialize(self, frame, rcvr, args):

        if (isinstance(self._som_node._specialize(frame, rcvr, args), GenericMessageNode)):
            return self._replace(MateGenericMessageNode(self._som_node))
        else:
            return self._replace(self._som_node)

    def execute(self, frame):

        rcvr, args = self._som_node._evaluate_rcvr_and_args(frame)
        return self._specialize(frame, rcvr, args).execute_evaluated(frame, rcvr, args)

    def reflective_op(self):
        return ReflectiveOp.MessageLookup