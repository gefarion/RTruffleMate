from som.vmobjects.abstract_object import AbstractObject
from som.interpreter.frame import Frame

class Context(AbstractObject):
    _immutable_fields_ = ["_frame"]

    def __init__(self, frame):
        AbstractObject.__init__(self)
        assert isinstance(frame, Frame)
        self._frame = frame

    def get_embedded_frame(self):
        return self._frame

    def __str__(self):
        return "\"" + self._frame + "\""

    def get_class(self, universe):
        return universe.contextClass
