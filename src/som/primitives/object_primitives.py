from rpython.rlib.objectmodel import compute_identity_hash
from rpython.rlib.debug import attach_gdb

from som.primitives.primitives import Primitives
from som.vm.globals import nilObject, falseObject, trueObject

from som.vmobjects.object    import Object  
from som.vmobjects.primitive import Primitive
from som.vmobjects.array     import Array
from som.vmobjects.shape import Shape


def _equals(ivkbl, rcvr, args, call_frame):
    op1 = args[0]
    op2 = rcvr
    if op1 is op2:
        return trueObject
    else:
        return falseObject


def _hashcode(ivkbl, rcvr, args, call_frame):
    return ivkbl.get_universe().new_integer(
        compute_identity_hash(rcvr))


def _objectSize(ivkbl, rcvr, args, call_frame):
    size = 0
    
    if isinstance(rcvr, Object):
        size = rcvr.get_number_of_fields()
    elif isinstance(rcvr, Array):
        size = rcvr.get_number_of_indexable_fields()

    return ivkbl.get_universe().new_integer(size)


def _perform(ivkbl, rcvr, args, call_frame):
    selector = args[0]

    invokable = rcvr.get_class(ivkbl.get_universe()).lookup_invokable(selector)
    return invokable.invoke(rcvr, [], call_frame)


def _performInSuperclass(ivkbl, rcvr, args, call_frame):
    clazz    = args[1]
    selector = args[0]

    invokable = clazz.lookup_invokable(selector)
    return invokable.invoke(rcvr, [], call_frame)


def _performWithArguments(ivkbl, rcvr, args, call_frame):
    arg_arr  = args[1].as_argument_array()
    selector = args[0]

    invokable = rcvr.get_class(ivkbl.get_universe()).lookup_invokable(selector)
    return invokable.invoke(rcvr, arg_arr, call_frame)


def _instVarAt(ivkbl, rcvr, args, call_frame):
    idx  = args[0]
    return rcvr.get_field(idx.get_embedded_integer() - 1)


def _instVarAtPut(ivkbl, rcvr, args, call_frame):
    val  = args[1]
    idx  = args[0]
    rcvr.set_field(idx.get_embedded_integer() - 1, val)
    return val

def _instVarNamedPut(ivkbl, rcvr, args, call_frame):
    i = rcvr.get_field_index(args[0])
    val  = args[1]
    rcvr.set_field(i, val)
    return rcvr

def _instVarNamed(ivkbl, rcvr, args, call_frame):
    i = rcvr.get_field_index(args[0])
    return rcvr.get_field(i)


def _halt(ivkbl, rcvr, args, call_frame):
    # noop
    print "BREAKPOINT"
    attach_gdb()
    return rcvr


def _class(ivkbl, rcvr, args, call_frame):
    return rcvr.get_class(ivkbl.get_universe())

def _set_meta_object_environment(ivkbl, rcvr, args, call_frame):
    rcvr.set_meta_object_environment(args[0])
    return rcvr

def _has_meta_object_environment(ivkbl, rcvr, args, call_frame):
    environment = rcvr.get_meta_object_environment()

    # No esta definido o es Nil
    if environment is None or not isinstance(environment, Object):
        return falseObject
    else:
        return trueObject

def _in_meta(ivkbl, rcvr, args, call_frame):
    if call_frame.meta_level():
        return trueObject
    else:
        return falseObject

def _shape(ivkbl, rcvr, args, meta_level):
    return Shape(rcvr.get_object_layout())


def _change_shape(ivkbl, rcvr, args, meta_level):
    shape = args[0]
    assert isinstance(shape, Shape)

    rcvr._set_layout_and_transfer_fields(shape.get_embedded_object_layout())
    return rcvr

class ObjectPrimitives(Primitives):
    
    def install_primitives(self):
        self._install_instance_primitive(Primitive("==", self._universe, _equals))
        self._install_instance_primitive(Primitive("hashcode", self._universe, _hashcode))
        self._install_instance_primitive(Primitive("objectSize", self._universe, _objectSize))
        self._install_instance_primitive(Primitive("perform:", self._universe, _perform))
        self._install_instance_primitive(Primitive("perform:inSuperclass:", self._universe, _performInSuperclass))
        self._install_instance_primitive(Primitive("perform:withArguments:", self._universe, _performWithArguments))
        self._install_instance_primitive(Primitive("instVarAt:", self._universe, _instVarAt))
        self._install_instance_primitive(Primitive("instVarAt:put:", self._universe, _instVarAtPut))
        self._install_instance_primitive(Primitive("instVarNamed:",  self._universe, _instVarNamed))
        self._install_instance_primitive(Primitive("instVarNamed:put:",  self._universe, _instVarNamedPut))
        
        self._install_instance_primitive(Primitive("halt",  self._universe, _halt))
        self._install_instance_primitive(Primitive("class", self._universe, _class))
        self._install_instance_primitive(Primitive("shape", self._universe, _shape))
        self._install_instance_primitive(Primitive("changeShape:", self._universe, _change_shape))

        self._install_instance_primitive(Primitive("installEnvironment:",  self._universe, _set_meta_object_environment))
        self._install_instance_primitive(Primitive("hasMetaObjectEnvironment",  self._universe, _has_meta_object_environment))
        self._install_instance_primitive(Primitive("inMeta",  self._universe, _in_meta))


