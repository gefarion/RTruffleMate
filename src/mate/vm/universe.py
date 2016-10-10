from som.vm.universe import Universe
from rlib.exit import Exit
from rpython.rlib import jit
from mate.interpreter.mateify_visitor import MateifyVisitor

class MateUniverse(Universe):

    def mateify(self, clazz):
        visitor = MateifyVisitor()

        invokables = clazz.get_instance_invokables()
        for i in xrange(0 , invokables.get_number_of_indexable_fields()):
            invokable = invokables.get_indexable_field(i)
            if not invokable.is_primitive():
                invokable.get_invokable().accept(visitor)

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