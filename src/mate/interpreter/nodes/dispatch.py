from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp


class MateUninitializedDispatchNode(MateNode):

    def reflective_op(self):
    	return ReflectiveOp.MessageActivation 


class MateGenericDispatchNode(MateNode):

    def reflective_op(self):
    	return ReflectiveOp.MessageActivation 


class MateSuperDispatchNode(MateNode):

    def reflective_op(self):
    	return ReflectiveOp.MessageActivation