from mate.vm.constants import ReflectiveOp
import som.vm.universe

class MOPDispatcher(object):

	Semantics_IDX = 0
	Layout_IDX    = 1
	Message_IDX   = 2

	@staticmethod
	def lookup_invokable(reflective_op, enviroment):
		metaClass = MOPDispatcher.meta_class_for_operation(reflective_op, enviroment)
		if not metaClass:
			return None

		selector = MOPDispatcher.selector_for_operation(reflective_op)
		if not selector:
			return None

		return metaClass.get_class(som.vm.universe.get_current()).lookup_invokable(selector)

	@staticmethod
	def selector_for_operation(reflective_op):

		selectors = {
			ReflectiveOp.MessageLookup:      "find:since:",
			ReflectiveOp.MessageActivation:  "activate:withArguments:",

			ReflectiveOp.ExecutorReadField:  "read:", # Listo
			ReflectiveOp.ExecutorWriteField: "write:value:", # Listo

			ReflectiveOp.ExecutorReturn:     "return:",

			ReflectiveOp.ExecutorLocalArg:   "readLocalArgument:inFrame:", # Listo

			ReflectiveOp.ExecutorReadLocal:  "readLocal:inFrame:",
			ReflectiveOp.ExecutorWriteLocal: "writeLocal:inFrame:value:",

			ReflectiveOp.LayoutReadField:    "read:",
			ReflectiveOp.LayoutWriteField:   "write:value:",
		}

		return som.vm.universe.get_current().symbol_for(selectors[reflective_op])

	@staticmethod
	def meta_class_for_operation(reflective_op, enviroment):

		field_idx = None
		if reflective_op <= ReflectiveOp.ExecutorReturn:
			field_idx = MOPDispatcher.Semantics_IDX
		elif reflective_op <= ReflectiveOp.MessageActivation:
			field_idx = MOPDispatcher.Message_IDX
		elif reflective_op <= ReflectiveOp.LayoutWriteField:
			field_idx = MOPDispatcher.Layout_IDX

		assert(field_idx)

		return enviroment.get_field(field_idx)
