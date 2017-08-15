from mate.vm.constants import ReflectiveOp

class MOPDispatcher(object):

	Semantics_IDX = 0
	Layout_IDX    = 1
	Message_IDX   = 2

	@staticmethod
	def lookup_invokable(universe, reflective_op, enviroment):

		metaclass = MOPDispatcher.meta_class_for_operation(reflective_op, enviroment)
		if not metaclass:
			return None

		selector = MOPDispatcher.selector_for_operation(universe, reflective_op)
		if not selector:
			return None

		return metaclass.get_class(universe).lookup_invokable(selector)

	@staticmethod
	def selector_for_operation(universe, reflective_op):

		selectors = {
			ReflectiveOp.MessageLookup:      "find:since:",
			ReflectiveOp.MessageActivation:  "activate:withArguments:withSemantics:",

			ReflectiveOp.ExecutorReadField:  "read:",
			ReflectiveOp.ExecutorWriteField: "write:value:",

			ReflectiveOp.ExecutorReturn:     "return:",

			ReflectiveOp.ExecutorLocalArg:   "readLocalArgument:inFrame:",

			ReflectiveOp.ExecutorReadLocal:  "readLocal:inFrame:",
			ReflectiveOp.ExecutorWriteLocal: "writeLocal:inFrame:value:",

			ReflectiveOp.LayoutReadField:    "read:",
			ReflectiveOp.LayoutWriteField:   "write:value:",
		}

		return universe.symbol_for(selectors[reflective_op])

	@staticmethod
	def meta_class_for_operation(reflective_op, enviroment):

		field_idx = None
		if reflective_op <= ReflectiveOp.ExecutorReturn:
			field_idx = MOPDispatcher.Semantics_IDX
		elif reflective_op <= ReflectiveOp.MessageActivation:
			field_idx = MOPDispatcher.Message_IDX
		elif reflective_op <= ReflectiveOp.LayoutWriteField:
			field_idx = MOPDispatcher.Layout_IDX
		else:
			raise ValueError("reflective op unknown")

		return enviroment.get_field(field_idx)
