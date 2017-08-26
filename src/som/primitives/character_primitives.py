from rpython.rlib.objectmodel import compute_hash

from som.primitives.primitives import Primitives
from som.vm.globals import falseObject, trueObject, nilObject
from som.vmobjects.primitive import Primitive
from som.vmobjects.string import String
from som.vmobjects.integer import Integer
from som.vmobjects.character import Character
from som.vmobjects.symbol import Symbol

def _as_integer(ivkbl, rcvr, args, meta_level):
    return ivkbl.get_universe().new_integer(ord(rcvr.get_embedded_character()))

def _as_string(ivkbl, rcvr, args, meta_level):
    return ivkbl.get_universe().new_string(rcvr.get_embedded_character())

def _is_digit(ivkbl, rcvr, args, meta_level):
    code = ord(rcvr.get_embedded_character())
    if code >= 48 and code <= 57:
        return trueObject
    else:
        return falseObject

def _is_letter(ivkbl, rcvr, args, meta_level):
    code = ord(rcvr.get_embedded_character())
    if (code >= 65 and code <= 90) or (code >= 97 and code <= 122): 
        return trueObject
    else:
        return falseObject

def _is_alphanumeric(ivkbl, rcvr, args, meta_level):
    code = ord(rcvr.get_embedded_character())
    if (code >= 48 and code <= 57) or (code >= 65 and code <= 90) or (code >= 97 and code <= 122): 
        return trueObject
    else:
        return falseObject

def _as_upper_case(ivkbl, rcvr, args, meta_level):
    return ivkbl.get_universe().new_character(rcvr.get_embedded_character().upper())

def _as_lower_case(ivkbl, rcvr, args, meta_level):
    return ivkbl.get_universe().new_character(rcvr.get_embedded_character().lower())

def _is_upper_case(ivkbl, rcvr, args, meta_level):
    code = ord(rcvr.get_embedded_character())
    if code >= 65 and code <= 90:
        return trueObject
    else:
        return falseObject

def _is_lower_case(ivkbl, rcvr, args, meta_level):
    code = ord(rcvr.get_embedded_character())
    if code >= 97 and code <= 122:
        return trueObject
    else:
        return falseObject

def _equals(ivkbl, rcvr, args, meta_level):
    other = args[0]

    if isinstance(other, Character):
        if rcvr.get_embedded_character() == other.get_embedded_character():
            return trueObject
        else:
            return falseObject

    if isinstance(other, String):
        if rcvr.get_embedded_character() == other.get_embedded_string():
            return trueObject
        else:
            return falseObject

    return falseObject

def _new(ivkbl, rcvr, args, meta_level):
    arg = args[0]
    if not isinstance(arg, Integer):
        return nilObject

    value = arg.get_embedded_integer()
    if value < 0 or value > 255:
        return nilObject

    return ivkbl.get_universe().new_character(chr(value))

class CharacterPrimitives(Primitives):
    
    def install_primitives(self):
        self._install_instance_primitive(Primitive("asInteger", self._universe, _as_integer))
        self._install_instance_primitive(Primitive("asString", self._universe, _as_string))
        self._install_instance_primitive(Primitive("isDigit", self._universe, _is_digit))
        self._install_instance_primitive(Primitive("isLetter", self._universe, _is_letter))
        self._install_instance_primitive(Primitive("isAlphaNumeric", self._universe, _is_alphanumeric))
        self._install_instance_primitive(Primitive("asUppercase", self._universe, _as_upper_case))
        self._install_instance_primitive(Primitive("asLowercase", self._universe, _as_lower_case))
        self._install_instance_primitive(Primitive("isUppercase", self._universe, _is_upper_case))
        self._install_instance_primitive(Primitive("isLowercase", self._universe, _is_lower_case))
        self._install_instance_primitive(Primitive("=", self._universe, _equals))
        self._install_class_primitive(Primitive("new:", self._universe, _new))