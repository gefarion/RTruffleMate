from som.interpreter.nodes.expression_node import ExpressionNode
from mate.interpreter.mop import MOPDispatcher
from mate.vm.constants import ReflectiveOp
from som.vmobjects.object import Object

class MateNode(ExpressionNode):

    _immutable_fields_ = ["_som_node?"]
    _child_nodes_ = ["_som_node"]

    def __init__(self, som_node, source_section = None):
        ExpressionNode.__init__(self, source_section)
        som_node.replace(self)
        self._som_node = self.adopt_child(som_node)

    def execute(self, frame):

        args = self._som_node.get_execute_args(frame)
        value = self.do_mate_semantics(frame, args)

        if value is None:
            return self._som_node.execute_prevaluated(frame, args)
        else:
            return value

    def mop_arguments(self, frame):
        raise NotImplementedError("Subclasses need to implement mop_arguments(self).")

    def do_mate_semantics(self, frame, args):
        assert frame is not None

        environment = args[0].get_meta_object_environment() or frame.get_meta_object_environment()

        # No esta definido
        if environment is None:
            return None

        # No es nil (TODO: Ver como mejorar esto)
        if not isinstance(environment, Object):
            return None

        print "[MATE] Encontrado environmentMO para " + str(self) + ", buscando metodo..."

        method = MOPDispatcher.lookup_invokable(self.reflective_op(), environment)
        if method is None:
            print "[MATE] Metodo no encontrado"
            return None
        else:
            print "[MATE] Metodo " + str(method) + " encontrado " + " ejecutando con " + str(args)

            # Tengo que desactivar mate para evitar recursion infinita, ver como implementar una solucion con niveles de contexto
            args[0].set_meta_object_environment(None)

            return method.invoke(args[0], args[1:])
