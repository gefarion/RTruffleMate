from mate.interpreter.nodes.mate_node import MateNode
from mate.vm.constants import ReflectiveOp


class MateUninitializedDispatchNode(MateNode):
    
    def reflectiveOp(self):
    	return ReflectiveOp.MessageActivation 


class MateGenericDispatchNode(MateNode):

    def reflectiveOp(self):
    	return ReflectiveOp.MessageActivation 


class MateSuperDispatchNode(MateNode):

    def reflectiveOp(self):
    	return ReflectiveOp.MessageActivation