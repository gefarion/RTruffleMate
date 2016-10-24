from som.vm.universe import Universe
from rlib.exit import Exit
from rpython.rlib import jit
from mate.interpreter.mateify_visitor import MateifyVisitor

class MateUniverse(Universe):

    _immutable_fields_ = [
            "objectClass",
            "classClass",
            "metaclassClass",
            "nilClass",
            "integerClass",
            "arrayClass",
            "methodClass",
            "symbolClass",
            "primitiveClass",
            "systemClass",
            "blockClass",
            "blockClasses[*]",
            "stringClass",
            "doubleClass",
            "environmentMO",
            "operationalSemanticsMO",
            "messageMO",
            "ShapeClass",
            "_symbol_table",
            "_globals",
            "_object_system_initialized"]

    def _initialize_object_system(self):

        system_object = Universe._initialize_object_system(self)

        self.environmentMO          = self.new_system_class()
        self.operationalSemanticsMO = self.new_system_class()
        self.messageMO              = self.new_system_class()
        self.shapeClass             = self.new_system_class()

        self._initialize_system_class(self.environmentMO, self.objectClass, "EnvironmentMO")
        self._initialize_system_class(self.operationalSemanticsMO, self.objectClass, "OperationalSemanticsMO")
        self._initialize_system_class(self.messageMO, self.objectClass, "MessageMO")
        self._initialize_system_class(self.shapeClass, self.objectClass, "Shape")

        self._load_system_class(self.environmentMO)
        self._load_system_class(self.operationalSemanticsMO)
        self._load_system_class(self.messageMO)
        self._load_system_class(self.shapeClass)

        return system_object

    def mateify(self, clazz):
        visitor = MateifyVisitor()

        invokables = clazz.get_instance_invokables()
        for i in xrange(0 , invokables.get_number_of_indexable_fields()):
            invokable = invokables.get_indexable_field(i)
            if not invokable.is_primitive():
                invokable.get_invokable().accept(visitor)

    def mateify_method(method):
        if not method.is_primitive():
            method.get_invokable().accept(visitor);

    def load_class(self, name):
        # Check if the requested class is already in the dictionary of globals
        result = self.get_global(name)
        if result is not None:
            return result

        # Load the class
        result = Universe.load_class(self, name)
        self.mateify(result)
        if result.has_super_class():
            self.mateify(result.get_super_class())

        return result

    def _load_system_class(self, system_class):
        result = Universe._load_system_class(self, system_class)

        if result is None:
            return result

        self.mateify(result)
        if result.has_super_class():
            self.mateify(result.get_super_class())

_current = MateUniverse()

def error_print(msg):
    os.write(2, msg or "")


def error_println(msg = ""):
    os.write(2, msg + "\n")


def std_print(msg):
    os.write(1, msg or "")


def std_println(msg = ""):
    os.write(1, msg + "\n")


def main(args):
    jit.set_param(None, 'trace_limit', 15000)
    u = _current
    u.interpret(args[1:])
    u.exit(0)


def get_current():
    return _current

if __name__ == '__main__':
    raise RuntimeError("Universe should not be used as main anymore")