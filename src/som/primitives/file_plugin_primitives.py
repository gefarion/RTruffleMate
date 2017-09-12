from som.primitives.primitives import Primitives
from som.vm.globals import falseObject, trueObject, nilObject
from som.vmobjects.primitive import Primitive
import os


def _image_file(ivkbl, rcvr, args, meta_level):
    return ivkbl.get_universe().new_string(os.getcwd() + "/RTruffleMate")

class FilePluginPrimsPrimitives(Primitives):

    def install_primitives(self):
        self._install_instance_primitive(Primitive("imageFile", self._universe, _image_file))