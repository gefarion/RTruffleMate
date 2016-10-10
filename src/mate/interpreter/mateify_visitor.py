class MateifyVisitor(object):

	def visitNode(self, node):
		return True

	def visitInvokable(self, node):
		return True

	def visitSequenceNode(self, node):
		return True

	def visitUninitializedMessageNode(self, node):
		return True

	def visitBlockNodeWithContext(self, node):
		return True

	def visitLocalArgumentReadNode(self, node):
		return True

	def visitLocalSelfReadNode(self, node):
		return True

	def visitCatchNonLocalReturnNode(self, node):
		return True

	def visitUninitializedGlobalReadNode(self, node):
		return True

	def visitLiteralNode(self, node):
		return True

	def visitUninitializedWriteNode(self, node):
		return True

	def visitUninitializedReadNode(self, node):
		return True

	def visitBlockNode(self, node):
		return True

	def visitFieldWriteNode(self, node):
		return True

	def visit_UninitializedWriteFieldNode(self, node):
		return True

	def visitFieldReadNode(self, node):
		return True

	def visit_UninitializedReadFieldNode(self, node):
		return True

	def visitGenericMessageNode(self, node):
		return True

	def visit_CachedDispatchObjectCheckNode(self, node):
		return True

	def visitUninitializedDispatchNode(self, node):
		return True

	def visitCachedGlobalReadNode(self, node):
		return True

	def visitIfTrueIfFalseNode(self, node):
		return True

	def visitLocalSuperReadNode(self, node):
		return True

	def visitGenericDispatchNode(self, node):
		return True

	def visitConstantGlobalReadNode(self, node):
		return True
