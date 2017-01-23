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
        return True

    def visitLocalArgumentReadNode(self, node):
        node.replace(MateLocalArgumentReadNode(node))
        return True

    def visitLocalSelfReadNode(self, node):
        node.replace(MateLocalSelfReadNode(node))
        return True

    def visitUninitializedGlobalReadNode(self, node):
        node.replace(MateUninitializedGlobalReadNode(node))
        return True

    def visitUninitializedWriteNode(self, node):
        node.replace(MateUninitializedWriteNode(node))
        return True

    def visitUninitializedReadNode(self, node):
        node.replace(MateUninitializedReadNode(node))
        return True

    def visitFieldWriteNode(self, node):
        node.replace(MateFieldWriteNode(node))
        return True

    def visitFieldReadNode(self, node):
        node.replace(MateFieldReadNode(node))
        return True

    def visitGenericMessageNode(self, node):
        node.replace(MateGenericMessageNode(node))
        return True