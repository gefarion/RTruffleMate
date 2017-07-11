from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp
from som.vmobjects.integer import Integer
from mate.interpreter.mop import MOPDispatcher

from som.vmobjects.object import Object

class MateUninitializedAbstractFieldNode(MateNode):

    def do_layout_mate_semantics(self, obj, value):
        assert obj is not None

        environment = obj.get_meta_object_environment()

        # No esta definido o es Nil
        if environment is None or not isinstance(environment, Object):
            return None

        method = MOPDispatcher.lookup_invokable(self.reflective_op(), environment)
        if method is None:
            # El mate enviroment no define el methodo correspondiente a este nodo
            return None

        # Tengo que desactivar mate para evitar recursion infinita, ver como implementar una solucion con niveles de contexto
        obj.set_meta_object_environment(None)
        res = method.invoke(obj, [Integer(self._som_node.field_idx() + 1), value])
        obj.set_meta_object_environment(environment)

        return res


class MateUninitializedReadFieldNode(MateUninitializedAbstractFieldNode):

    def read(self, obj):
        value = self.do_layout_mate_semantics(obj, None)

        if value is None:
            return self._som_node.read(obj)
        else:
            return value

    def reflective_op(self):
        return ReflectiveOp.LayoutReadField


class MateUninitializedWriteFieldNode(MateUninitializedAbstractFieldNode):

    def write(self, obj, value_to_write):
        value = self.do_layout_mate_semantics(obj, value_to_write)

        if value is None:
            return self._som_node.write(obj, value_to_write)
        else:
            return value

    def reflective_op(self):
        return ReflectiveOp.LayoutWriteField
