from rtruffle.node import Node
from mate.interpreter.mop import MOPDispatcher

class _AbstractMateLookUpNode(Node):

    INLINE_CACHE_SIZE = 10

    _immutable_fields_ = ['_universe']

    def __init__(self, universe):
        Node.__init__(self, None)
        self._universe = universe

class _AbstractMateLookUpWithReflectiveOp(_AbstractMateLookUpNode):

    _immutable_fields_ = ['reflective_op']

    def __init__(self, reflective_op, universe):
        _AbstractMateLookUpNode.__init__(self, universe)
        self._reflective_op = reflective_op


class UninitializedMateLookUpNode(_AbstractMateLookUpWithReflectiveOp):

    def _specialize(self, environment):
        assert environment is not None

        # Determine position in dispatch node chain, i.e., size of inline cache
        i_node = self
        chain_depth = 0

        while isinstance(i_node.get_parent(), _AbstractMateLookUpNode):
            i_node = i_node.get_parent()
            chain_depth += 1

        send_node = i_node.get_parent()

        if chain_depth < _AbstractMateLookUpNode.INLINE_CACHE_SIZE:

            method = MOPDispatcher.lookup_invokable(self._universe, self._reflective_op, environment)
            new_chain_end = UninitializedMateLookUpNode(self._reflective_op, self._universe)

            node = _CachedMateLookUpObjectCheckNode(environment, method, new_chain_end, self._universe)

            return self.replace(node)
        else:

            generic_replacement = _GenericMateLookUpNode(self._reflective_op, self._universe)
            send_node.replace_lookup_list_head(generic_replacement)
            return generic_replacement

    def lookup_meta_invokable(self, environment):
        return self._specialize(environment).lookup_meta_invokable(environment)


class _GenericMateLookUpNode(_AbstractMateLookUpWithReflectiveOp):

    def lookup_meta_invokable(self, environment):
    	return MOPDispatcher.lookup_invokable(self._universe, self._reflective_op, environment)


class _CachedMateLookUpObjectCheckNode(_AbstractMateLookUpNode):

    _immutable_fields_ = ['_cached_method', '_next?', '_expected_environment']
    _child_nodes_      = ['_next']

    def __init__(self, environment, method, next_dispatch, universe):
        _AbstractMateLookUpNode.__init__(self, universe)
        self._cached_method  = method
        self._next           = self.adopt_child(next_dispatch)
        self._expected_environment = environment

    def lookup_meta_invokable(self, environment):
        if environment == self._expected_environment:
            return self._cached_method
        else:
            return self._next.lookup_meta_invokable(environment)