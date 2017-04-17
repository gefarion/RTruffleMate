from som.primitives.primitives import Primitives
from som.vmobjects.abstract_object import AbstractObject
from som.vmobjects.primitive import Primitive
from som.vmobjects.context import Context
from som.vmobjects.integer import Integer

def _method(ivkbl, rcvr, args):
    assert False

def _sender(ivkbl, rcvr, args):
    assert False

def _receiver(ivkbl, rcvr, args):
    return rcvr.get_embedded_frame().get_self()

def _local_at(ivkbl, rcvr, args):
    index = args[0]
    assert isinstance(index, Integer)

    return rcvr.get_embedded_frame().get_temp(index)

def _arg_at(ivkbl, rcvr, args):
    index = args[0]
    assert isinstance(index, Integer)

    return rcvr.get_embedded_frame().get_argument(index)

def _local_at_put(ivkbl, rcvr, args):
    index = args[0]
    assert isinstance(index, Integer)

    value = args[1]
    assert isinstance(index, AbstractObject)

    return rcvr.get_embedded_frame().set_temp(index, value)

class ContextPrimitives(Primitives):
    
    def install_primitives(self):        
        self._install_instance_primitive(Primitive("method", self._universe, _method))
        self._install_instance_primitive(Primitive("sender", self._universe, _sender))
        self._install_instance_primitive(Primitive("receiver", self._universe, _receiver))
        self._install_instance_primitive(Primitive("localAt:", self._universe, _local_at))
        self._install_instance_primitive(Primitive("argAt", self._universe, _arg_at))
        self._install_instance_primitive(Primitive("localAt:put:", self._universe, _local_at_put))

