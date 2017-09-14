from som.primitives.primitives import Primitives
from som.vm.globals import falseObject, trueObject, nilObject
from som.vmobjects.primitive import Primitive
from som.vmobjects.file import File
from som.vmobjects.string import String
from som.vmobjects.integer import Integer
from som.vmobjects.array import Array
import os

def _stdio_handles(ivkbl, rcvr, args, meta_level):
    # TODo
    return nilObject

class FileStreamPrimitives(Primitives):

    def install_primitives(self):
        self._install_class_primitive(Primitive("stdioHandles", self._universe, _stdio_handles))
