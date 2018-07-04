from rpython.rlib import jit
from som.vmobjects.block import Block
from som.vmobjects.method import Method
from som.vmobjects.primitive   import Primitive
from som.primitives.primitives import Primitives
from rpython.rlib.debug import attach_gdb


def _at(ivkbl, rcvr, args, call_frame):
    i    = args[0]
    try:
        return  rcvr.get_indexable_field(i.get_embedded_integer() - 1)
    except:
        attach_gdb()


def _atPut(ivkbl, rcvr, args, call_frame):
    value = args[1]
    index = args[0]

    rcvr.set_indexable_field(index.get_embedded_integer() - 1, value)
    return value


def _length(ivkbl, rcvr, args, call_frame):
    return ivkbl.get_universe().new_integer(
        rcvr.get_number_of_indexable_fields())


def _new(ivkbl, rcvr, args, call_frame):
    length = args[0]

    return ivkbl.get_universe().new_array_with_length(
        length.get_embedded_integer())


def get_do_index_printable_location(block_method):
    assert isinstance(block_method, Method)
    return "#doIndexes: %s" % block_method.merge_point_string()

do_index_driver = jit.JitDriver(
    greens=['block_method'], reds='auto',
    is_recursive=True,
    get_printable_location=get_do_index_printable_location)


def _doIndexes(ivkbl, rcvr, args, call_frame):
    block = args[0]
    block_method = block.get_method()
    universe = ivkbl.get_universe()

    i = 1
    length = rcvr.get_number_of_indexable_fields()
    while i <= length:  # the i is propagated to Smalltalk, so, start with 1
        do_index_driver.jit_merge_point(block_method = block_method)
        block_method.invoke(block, [universe.new_integer(i)], call_frame)
        i += 1


def get_do_printable_location(block_method):
    assert isinstance(block_method, Method)
    return "#doIndexes: %s" % block_method.merge_point_string()

do_driver = jit.JitDriver(greens=['block_method'], reds='auto',
                          get_printable_location=get_do_printable_location)


def _do(ivkbl, rcvr, args, call_frame):
    block = args[0]
    block_method = block.get_method()

    i = 0
    length = rcvr.get_number_of_indexable_fields()
    while i < length:  # the array itself is zero indexed
        do_driver.jit_merge_point(block_method = block_method)
        block_method.invoke(block, [rcvr.get_indexable_field(i)], call_frame)
        i += 1


def _copy(ivkbl, rcvr, args, call_frame):
    return rcvr.copy()


def _putAll(ivkbl, rcvr, args, call_frame):
    arg = args[0]
    if isinstance(arg, Block):
        rcvr.set_all_with_block(arg, call_frame)
        return rcvr

    ## It is a simple value, just put it into the array

    ## TODO: move to array, and adapt to use strategies
    rcvr.set_all(arg)
    return rcvr


class ArrayPrimitives(Primitives):
    
    def install_primitives(self):
        self._install_instance_primitive(Primitive("at:",     self._universe, _at))
        self._install_instance_primitive(Primitive("at:put:", self._universe, _atPut))
        self._install_instance_primitive(Primitive("length",  self._universe, _length))
        self._install_instance_primitive(Primitive("copy",    self._universe, _copy))

        self._install_instance_primitive(Primitive("doIndexes:", self._universe, _doIndexes))
        self._install_instance_primitive(Primitive("do:",        self._universe, _do))
        self._install_instance_primitive(Primitive("putAll:",    self._universe, _putAll))

        self._install_class_primitive(Primitive("new:",       self._universe, _new))
