from mate.vm.constants import ReflectiveOp
from rpython.rlib import jit
from rpython.rlib.debug import make_sure_not_resized

SEMANTICS_IDX = 0
LAYOUT_IDX    = 1
MESSAGE_IDX   = 2

SELECTORS = [
	None, # Unused
	"read:", # ExecutorReadField
	"write:value:", # ExecutorWriteField
	"readLocal:inFrame:", # ExecutorReadLocal
	"writeLocal:inFrame:value:", # ExecutorWriteLocal
	"readLocalArgument:inFrame:", # ExecutorLocalArg
	None, # ExecutorNonLocalArg
	None, # ExecutorLocalSuperArg
	None, # ExecutorNonLocalSuperArg
	None, # ExecutorReadNonLocalTemp
	None, # ExecutorWriteNonLocalTemp
	None, # ExecutorNonLocalSelf
	None, # ExecutorLocalSelf
	None, # ExecutorLocalSuper
	"return:", # ExecutorReturn
	"find:since:", # MessageLookup
	"activate:withArguments:withSemantics:", # MessageActivation
	"read:", # LayoutReadField
	"write:value:" # LayoutWriteField
]

make_sure_not_resized(SELECTORS)

# @jit.elidable
def lookup_invokable(universe, reflective_op, enviroment):

	metaclass = meta_class_for_operation(reflective_op, enviroment)
	if not metaclass:
		return None

	selector = get_selector(universe, reflective_op)
	if not selector:
		return None

	return metaclass.get_class(universe).lookup_invokable(selector)

# @jit.elidable
def get_selector(universe, reflective_op):
	return universe.symbol_for(SELECTORS[reflective_op])

# @jit.elidable
def meta_class_for_operation(reflective_op, enviroment):

	field_idx = None
	if reflective_op <= ReflectiveOp.ExecutorReturn:
		field_idx = SEMANTICS_IDX
	elif reflective_op <= ReflectiveOp.MessageActivation:
		field_idx = MESSAGE_IDX
	elif reflective_op <= ReflectiveOp.LayoutWriteField:
		field_idx = LAYOUT_IDX
	else:
		raise ValueError("reflective op unknown")

	return enviroment.get_field(field_idx)
