from mate.vm.constants import ReflectiveOp
from mate.vm.universe import Universe

class MOPDispatcher(object):

	Semantics_IDX = 0
	Layout_IDX    = 1
	Message_IDX   = 2

	@staticmethod
	def lookupInvokable(reflectiveOp, enviromentMO):
		metaClass = self.metaClassForOperation(reflectiveOp, enviromentMO)
		if not metaClass:
			return None

		selector = self.selectorForOperation(reflectiveOp)
		if not selector:
			return None

		return metaClass.get_class(Universe.get_current()).lookup_invokable(selector)

	@staticmethod
	def selectorForOperation(reflectiveOp):

		selectors = {
			ReflectiveOp.MessageLookup:      "find:since:",
			ReflectiveOp.MessageActivation:  "activate:withArguments:",
			ReflectiveOp.ExecutorReadField:  "read:",
			ReflectiveOp.ExecutorWriteField: "write:value:",
			ReflectiveOp.ExecutorReturn:     "return:",
			ReflectiveOp.ExecutorLocalArg:   "localArgument:inFrame:",
			ReflectiveOp.ExecutorReadLocal:  "readLocal:inFrame:",
			ReflectiveOp.ExecutorWriteLocal: "writeLocal:inFrame:",
			ReflectiveOp.LayoutReadField:    "read:",
			ReflectiveOp.LayoutWriteField:   "write:value:",
		}

		return Universe.get_current().symbol_for(selectors[reflectiveOp])

	@staticmethod
	def metaclassForOperation(reflectiveOp, enviromentMO):

		field_idx = None
		if reflectiveOp <= 14:
			field_idx = Semantics_IDX
		elif reflectiveOp <= 16:
			field_idx = Message_IDX
		elif reflectiveOp <= 18:
			field_idx = Layout_IDX

		assert(field_idx)

		return enviromentMO.get_field(field_idx)
