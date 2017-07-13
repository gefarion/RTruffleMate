from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp
from som.vmobjects.integer import Integer

class MateFieldReadNode(MateNode):

    def get_meta_args(self, frame):
        return [Integer(self._som_node.field_idx() + 1)]

    def reflective_op(self):
        return ReflectiveOp.ExecutorReadField


class MateFieldWriteNode(MateNode):

    def get_meta_args(self, frame):
        return [Integer(self._som_node.field_idx() + 1), self._som_node.value(frame)]

    def reflective_op(self):
        return ReflectiveOp.ExecutorWriteField
