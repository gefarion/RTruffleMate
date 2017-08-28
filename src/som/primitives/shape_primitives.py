from som.primitives.primitives import Primitives
from som.vmobjects.abstract_object import AbstractObject
from som.vmobjects.primitive import Primitive
from som.vmobjects.shape import Shape
from som.vmobjects.integer import Integer
from som.vmobjects.clazz import Class
from som.interpreter.objectstorage.object_layout import ObjectLayout

def _fields_count(ivkbl, rcvr, args, meta_level):

    layout = rcvr.get_embedded_object_layout()
    return ivkbl.get_universe().new_integer(layout.get_number_of_fields())

def _install_environment(ivkbl, rcvr, args, meta_level):
    environment = args[0]
    return Shape(rcvr.get_embedded_object_layout().clone_with_environment(environment))

def _install_class(ivkbl, rcvr, args, meta_level):
    clazz = args[0]
    assert isinstance(clazz, Class)

    return Shape(rcvr.get_embedded_object_layout().clone_with_class(clazz))

def _new_with_fields_count(ivkbl, rcvr, args, meta_level):

    number_of_fields = args[0]
    assert isinstance(number_of_fields, Integer)

    return ivkbl.get_universe().new_shape(ObjectLayout(number_of_fields.get_embedded_integer()))

class ShapePrimitives(Primitives):

    def install_primitives(self):
        self._install_instance_primitive(Primitive("fieldsCount", self._universe, _fields_count))
        self._install_instance_primitive(Primitive("installEnvironment:", self._universe, _install_environment))
        self._install_instance_primitive(Primitive("installClass:", self._universe, _install_class))
        self._install_class_primitive(Primitive("newWithFieldsCount:", self._universe, _new_with_fields_count))
