from som.primitives.primitives import Primitives
from som.vmobjects.abstract_object import AbstractObject
from som.vmobjects.primitive import Primitive
from som.vmobjects.context import Context
from som.vmobjects.integer import Integer
from som.vmobjects.string import String
from som.interpreter.frame import Frame

def _method(ivkbl, rcvr, args, call_frame):
    assert False

def _sender(ivkbl, rcvr, args, call_frame):
    assert False

def _receiver(ivkbl, rcvr, args, call_frame):
    assert isinstance(rcvr, Context)

    frame = rcvr.get_embedded_frame()
    assert isinstance(frame, Frame)

    return frame.get_self()

def _local_at(ivkbl, rcvr, args, call_frame):
    assert isinstance(rcvr, Context)

    frame = rcvr.get_embedded_frame()
    assert isinstance(frame, Frame)

    index = args[0]
    assert isinstance(index, Integer)

    i = index.get_embedded_integer()

    return frame.get_temp(i - 1)

def _arg_at(ivkbl, rcvr, args, call_frame):
    assert isinstance(rcvr, Context)

    frame = rcvr.get_embedded_frame()
    assert isinstance(frame, Frame)

    index = args[0]
    assert isinstance(index, Integer)

    i = index.get_embedded_integer()
    return frame.get_argument(i - 1)

def _local_at_put(ivkbl, rcvr, args, call_frame):
    assert isinstance(rcvr, Context)

    frame = rcvr.get_embedded_frame()
    assert isinstance(frame, Frame)

    index = args[0]
    assert isinstance(index, Integer)

    value = args[1]
    assert isinstance(value, AbstractObject)

    i = index.get_embedded_integer()
    frame.set_temp(i - 1, value)

    return rcvr

class ContextPrimitives(Primitives):

    def install_primitives(self):
        self._install_instance_primitive(Primitive("method", self._universe, _method))
        self._install_instance_primitive(Primitive("sender", self._universe, _sender))
        self._install_instance_primitive(Primitive("receiver", self._universe, _receiver))
        self._install_instance_primitive(Primitive("localAt:", self._universe, _local_at))
        self._install_instance_primitive(Primitive("argAt:", self._universe, _arg_at))
        self._install_instance_primitive(Primitive("localAt:put:", self._universe, _local_at_put))

