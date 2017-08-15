from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp
from som.vmobjects.integer import Integer
from mate.interpreter.mop import MOPDispatcher

from som.vmobjects.object import Object

class MateUninitializedAbstractFieldNode(MateNode):

    def do_layout_mate_semantics(self, frame, obj, value):
        assert obj is not None

        environment = frame.get_meta_object_environment() or obj.get_meta_object_environment()

        # No esta definido o es Nil
        if environment is None or not isinstance(environment, Object):
            return None

        method = self._lookup_node.lookup_meta_invokable(environment)
        if method is None:
            # El mate enviroment no define el methodo correspondiente a este nodo
            return None

        return method.invoke(obj, [Integer(self._som_node.field_idx() + 1), value], True)


class MateUninitializedReadFieldNode(MateUninitializedAbstractFieldNode):

    def read(self, frame, obj):

        value = None
        if not frame.meta_level():
            value = self.do_layout_mate_semantics(frame, obj, None)

        if value is None:
            return self._som_node.read(frame, obj)
        else:
            return value

    def reflective_op(self):
        return ReflectiveOp.LayoutReadField


class MateUninitializedWriteFieldNode(MateUninitializedAbstractFieldNode):

    def write(self, frame, obj, value_to_write):

        value = None
        if not frame.meta_level():
            value = self.do_layout_mate_semantics(frame, obj, value_to_write)

        if value is None:
            return self._som_node.write(frame, obj, value_to_write)
        else:
            return value

    def reflective_op(self):
        return ReflectiveOp.LayoutWriteField
