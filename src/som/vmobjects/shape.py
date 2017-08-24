from som.vmobjects.abstract_object import AbstractObject
from som.interpreter.objectstorage.object_layout import ObjectLayout

class Shape(AbstractObject):
    _immutable_fields_ = ["_object_layout"]

    def __init__(self, object_layout):
        AbstractObject.__init__(self)
        assert isinstance(object_layout, ObjectLayout)
        self._object_layout = object_layout

    def get_embedded_object_layout(self):
        return self._object_layout

    def __str__(self):
        return "\"" + self._frame + "\""

    def get_class(self, universe):
        return universe.shapeClass
