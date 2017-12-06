from som.primitives.primitives import Primitives
from som.vm.globals import nilObject, trueObject, falseObject

from som.vmobjects.abstract_object import AbstractObject
from som.vmobjects.array           import Array
from som.vmobjects.method          import Method
from som.vmobjects.primitive       import Primitive


def _holder(ivkbl, rcvr, args, call_frame):
    return rcvr.get_holder()

def _signature(ivkbl, rcvr, args, call_frame):
    return rcvr.get_signature()

def _is_primitive(ivkbl, rcvr, args, call_frame):
    return falseObject


def _invoke_on_with(ivkbl, rcvr, args, call_frame):
    assert isinstance(rcvr,    Method)
    assert isinstance(args[0], AbstractObject)
    assert isinstance(args[1], Array) or args[1] is nilObject

    if args[1] is nilObject:
        direct_args = []
    else:
        direct_args = args[1].as_argument_array()

    return rcvr.invoke(args[0], direct_args, call_frame)

def _invoke_mate_on_with_semantics(ivkbl, rcvr, args, call_frame):
    assert isinstance(rcvr,    Method)
    assert isinstance(args[0], AbstractObject)
    assert isinstance(args[1], Array) or args[1] is nilObject
    assert isinstance(args[2], AbstractObject)

    if args[1] is nilObject:
        direct_args = []
    else:
        direct_args = args[1].as_argument_array()

    return rcvr.invoke_from_mate(args[0], direct_args, call_frame, args[2])

def _invoke_mate_on_with(ivkbl, rcvr, args, call_frame):
    assert isinstance(rcvr,    Method)
    assert isinstance(args[0], AbstractObject)
    assert isinstance(args[1], Array) or args[1] is nilObject

    if args[1] is nilObject:
        direct_args = []
    else:
        direct_args = args[1].as_argument_array()

    return rcvr.invoke_from_mate(args[0], direct_args, call_frame)

class MethodPrimitives(Primitives):
    def install_primitives(self):
        self._install_instance_primitive(Primitive("holder",
                                                   self._universe, _holder))
        self._install_instance_primitive(Primitive("signature",
                                                   self._universe, _signature))
        self._install_instance_primitive(Primitive("isPrimitive",
                                                   self._universe, _is_primitive))
        self._install_instance_primitive(Primitive("invokeOn:with:",
                                                   self._universe, _invoke_on_with))
        self._install_instance_primitive(Primitive("invokeMateOn:with:",
                                                   self._universe, _invoke_mate_on_with))
        self._install_instance_primitive(Primitive("invokeMateOn:with:withSemantics:",
                                                   self._universe, _invoke_mate_on_with_semantics))
