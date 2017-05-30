from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp
from som.vmobjects.integer import Integer

class MateFieldReadNode(MateNode):

    def get_meta_args(self, frame):
        return [frame.get_self().get_field_name(self._som_node.field_idx())]

    def reflective_op(self):
        return ReflectiveOp.ExecutorReadField


class MateFieldWriteNode(MateNode):

    def get_meta_args(self, frame):
        return [frame.get_self().get_field_name(self._som_node.field_idx()), self._som_node.value(frame)]

    def reflective_op(self):
        return ReflectiveOp.ExecutorWriteField
