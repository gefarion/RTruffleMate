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

    def visitUninitializedMessageNode(self, node):
        node.replace(MateUninitializedMessageNode.mateify(node))
        return True

    def visitLocalArgumentReadNode(self, node):
        node.replace(MateLocalArgumentReadNode.mateify(node))
        return True

    def visitLocalSelfReadNode(self, node):
        node.replace(MateLocalSelfReadNode.mateify(node))
        return True

    def visitUninitializedGlobalReadNode(self, node):
        node.replace(MateUninitializedGlobalReadNode.mateify(node))
        return True

    def visitUninitializedWriteNode(self, node):
        node.replace(MateUninitializedWriteNode.mateify(node))
        return True

    def visitUninitializedReadNode(self, node):
        node.replace(MateUninitializedReadNode.mateify(node))
        return True

    def visitFieldWriteNode(self, node):
        node.replace(MateFieldWriteNode.mateify(node))
        return True

    def visitFieldReadNode(self, node):
        node.replace(MateFieldReadNode.mateify(node))
        return True

    def visit_UninitializedWriteFieldNode(self, node):
        # Analizar el codigo para ver si realmente hay que convertirlos
        # node.replace(Mate_UninitializedWriteFieldNode.mateify(node))
        return True

    def visit_UninitializedReadFieldNode(self, node):
        # Analizar el codigo para ver si realmente hay que convertirlos
        # node.replace(Mate_UninitializedReadFieldNode.mateify(node))
        return True

    def visitGenericMessageNode(self, node):
        node.replace(MateGenericMessageNode.mateify(node))
        return True

    def visitLiteralNode(self, node):
        return True

    def visitBlockNodeWithContext(self, node):
        return True

    def visitNode(self, node):
        return True

    def visitInvokable(self, node):
        return True

    def visitSequenceNode(self, node):
        return True

    def visitBlockNode(self, node):
        return True

    def visitCatchNonLocalReturnNode(self, node):
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

    # NODOS DE MATE, NO SE CONVIERTEN

    def visitMateLocalSelfReadNode(self, node):
        return True

    def visitMateUninitializedGlobalReadNode(self, node):
        return True

    def visitMateUninitializedWriteNode(self, node):
        return True

    def visitMateUninitializedReadNode(self, node):
        return True

    def visitMateFieldWriteNode(self, node):
        return True

    def visitMateFieldReadNode(self, node):
        return True

    def visitMateGenericMessageNode(self, node):
        return True

    def visitMateLocalArgumentReadNode(self, node):
        return True

    def visitMateUninitializedMessageNode(self, node):
        return True
