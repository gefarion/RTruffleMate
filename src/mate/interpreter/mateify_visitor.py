from mate.interpreter.nodes.block_node import *
from mate.interpreter.nodes.contextual_node import *
from mate.interpreter.nodes.dispatch import *
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

class MateifyVisitor(object):

    def visitNode(self, node):
        return True

    def visitUninitializedMessageNode(self, node):
        node.replace(MateUninitializedMessageNode(node))

    def visitLocalArgumentReadNode(self, node):
        node.replace(MateLocalArgumentReadNode(node))

    def visitLocalSelfReadNode(self, node):
        node.replace(MateLocalSelfReadNode(node))

    def visitUninitializedGlobalReadNode(self, node):
        node.replace(MateUninitializedGlobalReadNode(node))

    def visitUninitializedWriteNode(self, node):
        node.replace(MateUninitializedWriteNode(node))

    def visitUninitializedReadNode(self, node):
        node.replace(MateUninitializedReadNode(node))

    def visitFieldWriteNode(self, node):
        node.replace(MateFieldWriteNode(node))

    def visitFieldReadNode(self, node):
        node.replace(MateFieldReadNode(node))

    def visitGenericMessageNode(self, node):
        node.replace(MateGenericMessageNode(node))

    def visitInvokable(self, node):
        pass

    def visitSequenceNode(self, node):
        pass
        
    def visitLocalUnsharedWriteNode(self, node):
        pass
        
    def visitLocalSharedWriteNode(self, node):
        pass
        
    def visit_LocalVariableWriteNode(self, node):
        pass
        
    def NonLocalTempWriteNode(self, node):
        pass
        
    def visitCachedGlobalReadNode(self, node):
        pass
        
    def visitConstantGlobalReadNode(self, node):
        pass
        
    def visitNonLocalArgumentReadNode(self, node):
        pass
        
    def visitLocalUnsharedTempReadNode(self, node):
        pass
        
    def visitLocalSharedTempReadNode(self, node):
        pass
        
    def visitNonLocalTempReadNode(self, node):
        pass
        
    def visit_NonLocalVariableReadNode(self, node):
        pass
        
    def visit_NonLocalVariableNode(self, node):
        pass
        
    def visitGenericDispatchNode(self, node):
        pass
        
    def visit_CachedDispatchObjectCheckNode(self, node):
        pass
        
    def visit_CachedDnuObjectCheckNode(self, node):
        pass
        
    def visitUninitializedDispatchNode(self, node):
        pass
        
    def visit_AbstractDispatchWithLookupNode(self, node):
        pass
        
    def visitSuperDispatchNode(self, node):
        pass
        
    def visit_LocalVariableNode(self, node):
        pass
        
    def visitUninitializedArgumentReadNode(self, node):
        pass
        
    def visitNonLocalSuperReadNode(self, node):
        pass
        
    def visitBlockNodeWithContext(self, node):
        pass
        
    def visitReturnNonLocalNode(self, node):
        pass
        
    def visitNonLocalSelfReadNode(self, node):
        pass
        
    def visitBlockNode(self, node):
        pass
        
    def visitLocalSuperReadNode(self, node):
        pass
        
    def visitCatchNonLocalReturnNode(self, node):
        pass
        
    def visitContextualNode(self, node):
        pass
        
    def visitLiteralNode(self, node):
        pass

    def visitExpressionNode(self, node):
        pass

    def visit_UninitializedReadFieldNode(self, node):
        pass

    def visit_GenericReadFieldNode(self, node):
        pass
        
    def visit_SpecializedReadFieldNode(self, node):
        pass
        
    def visit_GenericWriteFieldNode(self, node):
        pass
        
    def visit_SpecializedWriteFieldNode(self, node):
        pass
        
    def visit_UninitializedWriteFieldNode(self, node):
        pass
