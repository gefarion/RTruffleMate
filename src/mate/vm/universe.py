from som.vm.universe import Universe
from rlib.exit import Exit
from rpython.rlib import jit

class MateUniverse(Universe):
	pass

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