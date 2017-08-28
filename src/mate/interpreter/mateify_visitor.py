from mate.interpreter.nodes.block_node import *
from mate.interpreter.nodes.contextual_node import *
from mate.interpreter.nodes.expression_node import *
from mate.interpreter.nodes.field_node import *
from mate.interpreter.nodes.global_read_node import *
from mate.interpreter.nodes.literal_node import *
from mate.interpreter.nodes.return_non_local_node import *
from mate.interpreter.nodes.sequence_node import *
from mate.interpreter.nodes.variable_read_node import *
from mate.interpreter.nodes.message.abstract_node import *
from mate.interpreter.nodes.message.generic_node import *
from mate.interpreter.nodes.message.uninitialized_node import *
from mate.interpreter.nodes.message.generic_node import *
from mate.interpreter.invokable import *
from mate.interpreter.objectstorage.field_accessor_node import *

class MateifyVisitor(object):

    # Message MOP

    def visit_UninitializedMessageNode(self, node):
        MateGenericMessageNode(node)

    def visit_Invokable(self, node):
        if (not node.get_method().isSPECIAL()):
            MateInvokable(node)

    # Semantics MOP

    def visit_LocalArgumentReadNode(self, node):
        MateLocalArgumentReadNode(node)

    def visit_UninitializedWriteNode(self, node):
        MateUninitializedWriteNode(node)

    def visit_UninitializedReadNode(self, node):
        MateUninitializedReadNode(node)

    def visit_ReturnLocalNode(self, node):
        MateReturnLocalNode(node)

    def visit_FieldWriteNode(self, node):
        MateFieldWriteNode(node)

    def visit_FieldReadNode(self, node):
        MateFieldReadNode(node)

    def visit_ReturnNonLocalNode(self, node):
        return

    # Layout MOP

    def visit_UninitializedReadFieldNode(self, node):
        MateUninitializedReadFieldNode(node)
        pass

    def visit_UninitializedWriteFieldNode(self, node):
        MateUninitializedWriteFieldNode(node)
        pass

    # Otros nodos

    def visit_Node(self, node):
        pass

    def visit_UninitializedArgumentReadNode(self, node):
        pass

    def visit_CatchNonLocalReturnNode(self, node):
        pass

    def visit_UninitializedGlobalReadNode(self, node):
        pass

    def visit_LocalSelfReadNode(self, node):
        pass

    def visit_SequenceNode(self, node):
        pass

    def visit_LocalUnsharedWriteNode(self, node):
        pass

    def visit_LocalSharedWriteNode(self, node):
        pass

    def visit_LocalVariableWriteNode(self, node):
        pass

    def visit_NonLocalTempWriteNode(self, node):
        pass

    def visit_CachedGlobalReadNode(self, node):
        pass

    def visit_ConstantGlobalReadNode(self, node):
        pass

    def visit_NonLocalArgumentReadNode(self, node):
        pass

    def visit_LocalUnsharedTempReadNode(self, node):
        pass

    def visit_LocalSharedTempReadNode(self, node):
        pass

    def visit_NonLocalTempReadNode(self, node):
        pass

    def visit_NonLocalVariableReadNode(self, node):
        pass

    def visit_NonLocalVariableNode(self, node):
        pass

    def visit_GenericDispatchNode(self, node):
        pass

    def visit_CachedDispatchObjectCheckNode(self, node):
        pass

    def visit_CachedDnuObjectCheckNode(self, node):
        pass

    def visit_UninitializedDispatchNode(self, node):
        pass

    def visit_AbstractDispatchWithLookupNode(self, node):
        pass

    def visit_SuperDispatchNode(self, node):
        pass

    def visit_LocalVariableNode(self, node):
        pass

    def visit_NonLocalSuperReadNode(self, node):
        pass

    def visit_BlockNodeWithContext(self, node):
        pass

    def visit_NonLocalSelfReadNode(self, node):
        pass

    def visit_BlockNode(self, node):
        pass

    def visit_LocalSuperReadNode(self, node):
        pass

    def visit_ContextualNode(self, node):
        pass

    def visit_LiteralNode(self, node):
        pass

    def visit_ExpressionNode(self, node):
        pass

    def visit_GenericReadFieldNode(self, node):
        pass

    def visit_SpecializedReadFieldNode(self, node):
        pass

    def visit_GenericWriteFieldNode(self, node):
        pass

    def visit_SpecializedWriteFieldNode(self, node):
        pass

    def visit_GenericMessageNode(self, node):
        pass

    def visit_UninitializedDispatchNode(self, node):
        pass
