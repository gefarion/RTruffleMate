from som.primitives.primitives import Primitives
from som.vm.globals import falseObject, trueObject
from som.vmobjects.primitive       import Primitive

def _new(ivkbl, rcvr, args, call_frame):
    return ivkbl.get_universe().new_instance(rcvr)

def _new_with_environment(ivkbl, rcvr, args, call_frame):
    obj = ivkbl.get_universe().new_instance(rcvr)
    obj.set_meta_object_environment(args[0])
    return obj

def _name(ivkbl, rcvr, args, call_frame):
    return rcvr.get_name()


def _super_class(ivkbl, rcvr, args, call_frame):
    return rcvr.get_super_class()


def _methods(ivkbl, rcvr, args, call_frame):
    return rcvr.get_instance_invokables()

def _fields(ivkbl, rcvr, args, call_frame):
    return rcvr.get_instance_fields()

def _has_method(ivkbl, rcvr, args, call_frame):
    signature = args[0]

    invokables = rcvr.get_instance_invokables()
    ninvokables = invokables.get_number_of_indexable_fields()

    for i in xrange(0, ninvokables):
        invokable = invokables.get_indexable_field(i)
        if invokable.get_signature() == signature:
            return trueObject

    return falseObject

class ClassPrimitives(Primitives):
    def install_primitives(self):
        self._install_instance_primitive(Primitive("basicNew",   self._universe, _new))
        self._install_instance_primitive(Primitive("basicNew:",   self._universe, _new_with_environment))
        self._install_instance_primitive(Primitive("name",       self._universe, _name))
        self._install_instance_primitive(Primitive("superclass", self._universe, _super_class))
        self._install_instance_primitive(Primitive("methods",    self._universe, _methods))
        self._install_instance_primitive(Primitive("fields",     self._universe, _fields))
        self._install_instance_primitive(Primitive("hasMethod",  self._universe, _has_method))
