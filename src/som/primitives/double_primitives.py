from rpython.rlib.rfloat import round_double, INFINITY

from som.primitives.primitives import Primitives
from som.vmobjects.primitive   import Primitive
from som.vmobjects.double      import Double
from som.vmobjects.integer     import Integer

import math


def _coerce_to_double(obj, universe):
    if isinstance(obj, Double):
        return obj
    if isinstance(obj, Integer):
        return universe.new_double(float(obj.get_embedded_integer()))
    raise ValueError("Cannot coerce %s to Double!" % obj)


def _asString(ivkbl, rcvr, args, meta_level):
    return rcvr.prim_as_string(ivkbl.get_universe())


def _sqrt(ivkbl, rcvr, args, meta_level):
    return ivkbl.get_universe().new_double(
        math.sqrt(rcvr.get_embedded_double()))


def _plus(ivkbl, rcvr, args, meta_level):
    return rcvr.prim_add(args[0], ivkbl.get_universe())


def _minus(ivkbl, rcvr, args, meta_level):
    return rcvr.prim_subtract(args[0], ivkbl.get_universe())


def _mult(ivkbl, rcvr, args, meta_level):
    return rcvr.prim_multiply(args[0], ivkbl.get_universe())


def _doubleDiv(ivkbl, rcvr, args, meta_level):
    return rcvr.prim_double_div(args[0], ivkbl.get_universe())


def _mod(ivkbl, rcvr, args, meta_level):
    return rcvr.prim_modulo(args[0], ivkbl.get_universe())


def _equals(ivkbl, rcvr, args, meta_level):
    return rcvr.prim_equals(args[0], ivkbl.get_universe())


def _unequals(ivkbl, rcvr, args, meta_level):
    return rcvr.prim_unequals(args[0], ivkbl.get_universe())


def _lessThan(ivkbl, rcvr, args, meta_level):
    return rcvr.prim_less_than(args[0], ivkbl.get_universe())


def _lessThanOrEqual(ivkbl, rcvr, args, meta_level):
    return rcvr.prim_less_than_or_equal(args[0], ivkbl.get_universe())


def _greaterThan(ivkbl, rcvr, args, meta_level):
    return rcvr.prim_greater_than(args[0], ivkbl.get_universe())


def _round(ivkbl, rcvr, args, meta_level):
    int_value = int(round_double(rcvr.get_embedded_double(), 0))
    return ivkbl.get_universe().new_integer(int_value)


def _positive_infinity(ivkbl, rcvr, args, meta_level):
    return ivkbl.get_universe().new_double(INFINITY)


class DoublePrimitives(Primitives):

    def install_primitives(self):        
        self._install_instance_primitive(Primitive("asString", self._universe, _asString))
        self._install_instance_primitive(Primitive("round",    self._universe, _round))
        self._install_instance_primitive(Primitive("sqrt",     self._universe, _sqrt))
        self._install_instance_primitive(Primitive("+",        self._universe, _plus))
        self._install_instance_primitive(Primitive("-",        self._universe, _minus))
        self._install_instance_primitive(Primitive("*",        self._universe, _mult))
        self._install_instance_primitive(Primitive("//",       self._universe, _doubleDiv))
        self._install_instance_primitive(Primitive("%",        self._universe, _mod))
        self._install_instance_primitive(Primitive("=",        self._universe, _equals))
        self._install_instance_primitive(Primitive("<",        self._universe, _lessThan))
        self._install_instance_primitive(Primitive("<=",       self._universe, _lessThanOrEqual))
        self._install_instance_primitive(Primitive(">",        self._universe, _greaterThan))
        self._install_instance_primitive(Primitive("<>",       self._universe, _unequals))
        self._install_instance_primitive(Primitive("~=",       self._universe, _unequals))

        self._install_class_primitive(Primitive("PositiveInfinity", self._universe, _positive_infinity))
