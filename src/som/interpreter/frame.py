from rpython.rlib import jit
from rpython.rlib.debug import make_sure_not_resized
from som.vm.globals import nilObject


class _FrameOnStackMarker(object):

    def __init__(self):
        self._on_stack = True

    def mark_as_no_longer_on_stack(self):
        self._on_stack = False

    def is_on_stack(self):
        return self._on_stack

_EMPTY_LIST = []


class Frame(object):
        
    _immutable_fields_ = ['_receiver', '_arguments[*]', '_args_for_inner[*]',
                          '_temps', '_temps_for_inner', '_on_stack', '_meta_level']
    _virtualizable_    = ['_temps[*]']

    def __init__(self, receiver, arguments, arg_mapping, num_local_temps,
                 num_context_temps, meta_level=False):
        make_sure_not_resized(arguments)
        make_sure_not_resized(arg_mapping)
        self = jit.hint(self, access_directly=True, fresh_virtualizable=True)
        self._receiver        = receiver
        self._arguments       = arguments
        self._meta_object_environment = None
        self._on_stack        = _FrameOnStackMarker()
        self._meta_level = meta_level

        if num_local_temps == 0:
            self._temps       = _EMPTY_LIST
        else:
            self._temps       = [nilObject] * num_local_temps

        self._args_for_inner  = self._collect_shared_args(arg_mapping)
        if num_context_temps == 0:
            self._temps_for_inner = _EMPTY_LIST
        else:
            self._temps_for_inner = [nilObject] * num_context_temps

    @jit.unroll_safe
    def _collect_shared_args(self, arg_mapping):
        if len(arg_mapping) == 0:
            return _EMPTY_LIST
        return [self._arguments[i] for i in arg_mapping]

    def meta_level(self):
        return self._meta_level

    def get_context_values(self):
        return self._receiver, self._args_for_inner, self._temps_for_inner, self._on_stack

    def get_meta_object_environment(self):
        return self._meta_object_environment

    def set_meta_object_environment(self, environment):
        self._meta_object_environment = environment

    def get_argument(self, index):
        jit.promote(index)
        return self._arguments[index]

    def set_argument(self, index, value):
        self._arguments[index] = value

    def get_temp(self, index):
        jit.promote(index)
        temps = self._temps
        assert 0 <= index < len(temps)
        assert temps is not None
        return temps[index]

    def set_temp(self, index, value):
        jit.promote(index)
        temps = self._temps
        assert temps is not None
        assert 0 <= index < len(temps)
        temps[index] = value

    def get_shared_temp(self, index):
        jit.promote(index)
        temps = self._temps_for_inner
        assert 0 <= index < len(temps)
        assert temps is not None
        return temps[index]

    def set_shared_temp(self, index, value):
        jit.promote(index)
        temps = self._temps_for_inner
        assert temps is not None
        assert 0 <= index < len(temps)
        temps[index] = value

    def get_self(self):
        return self._receiver

    def get_on_stack_marker(self):
        return self._on_stack

    def __str__(self):
        return "Frame(%s, %s, %s)" % (self._receiver, self._arguments,
                                      self._temps)
