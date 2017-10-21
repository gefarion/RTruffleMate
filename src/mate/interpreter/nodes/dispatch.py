from rtruffle.node import Node


class _AbstractMateDispatchNode(Node):

    INLINE_CACHE_SIZE = 10

    _immutable_fields_ = ['_universe']

    def __init__(self, universe):
        Node.__init__(self, None)
        self._universe = universe

    def _accept(self, visitor):
        raise NotImplementedError("You cant visit this node")

class _AbstractMateDispatchWithLookupNode(_AbstractMateDispatchNode):

    _immutable_fields_ = ['_selector']

    def __init__(self, selector, universe):
        _AbstractMateDispatchNode.__init__(self, universe)
        self._selector = selector

class UninitializedMateDispatchNode(_AbstractMateDispatchWithLookupNode):

    def _specialize(self, rcvr, lookup_method, call_frame):
        assert rcvr is not None

        # Determine position in dispatch node chain, i.e., size of inline cache
        i_node = self
        chain_depth = 0

        while isinstance(i_node.get_parent(), _AbstractMateDispatchNode):
            i_node = i_node.get_parent()
            chain_depth += 1

        send_node = i_node.get_parent()

        if chain_depth < _AbstractMateDispatchNode.INLINE_CACHE_SIZE:

            rcvr_class = rcvr.get_class(self._universe)
            method = lookup_method.invoke_to_mate(rcvr, [self._selector, rcvr_class], call_frame)

            new_chain_end = UninitializedMateDispatchNode(self._selector,
                                                      self._universe)

            if method is not None:
                node = _CachedMateDispatchObjectCheckNode(rcvr_class, method,
                                                      new_chain_end,
                                                      self._universe)
            else:
                node = _CachedMateDnuObjectCheckNode(self._selector, rcvr_class,
                                                 new_chain_end, self._universe)

            return self.replace(node)
        else:
            # the chain is longer than the maximum defined by INLINE_CACHE_SIZE
            # and thus, this callsite is considered to be megaprophic, and we
            # generalize it.

            generic_replacement = GenericMateDispatchNode(self._selector,
                                                      self._universe)
            send_node.replace_mate_dispatch_list_head(generic_replacement)
            return generic_replacement

    def execute_mate_dispatch(self, rcvr, args, call_frame, lookup_method):
        return self._specialize(rcvr, lookup_method, call_frame).execute_mate_dispatch(rcvr, args, call_frame, lookup_method)

class GenericMateDispatchNode(_AbstractMateDispatchWithLookupNode):

    def execute_mate_dispatch(self, rcvr, args, call_frame, lookup_method):

        method = lookup_method.invoke_to_mate(rcvr, [self._selector, rcvr.get_class(self._universe)], call_frame)
        if method is not None:
            return method.invoke(rcvr, args, call_frame)
        else:
            # Won't use DNU caching here, because it's a megamorphic node
            return rcvr.send_does_not_understand(self._selector, args,
                                                 self._universe, call_frame)

class _AbstractCachedMateDispatchNode(_AbstractMateDispatchNode):

    _immutable_fields_ = ['_cached_method', '_next?', '_expected_class']
    _child_nodes_      = ['_next']

    def __init__(self, rcvr_class, method, next_dispatch, universe):
        _AbstractMateDispatchNode.__init__(self, universe)
        self._cached_method  = method
        self._next           = self.adopt_child(next_dispatch)
        self._expected_class = rcvr_class

class _CachedMateDispatchObjectCheckNode(_AbstractCachedMateDispatchNode):

    def execute_mate_dispatch(self, rcvr, args, call_frame, lookup_method):
        if rcvr.get_class(self._universe) == self._expected_class:
            return self._cached_method.invoke(rcvr, args, call_frame)
        else:
            return self._next.execute_mate_dispatch(rcvr, args, call_frame, lookup_method)

class _CachedMateDnuObjectCheckNode(_AbstractCachedMateDispatchNode):

    _immutable_fields_ = ['_selector']

    def __init__(self, selector, rcvr_class, next_dispatch, universe):
        _AbstractCachedMateDispatchNode.__init__(
            self, rcvr_class, rcvr_class.lookup_invokable(
                universe.symbol_for("doesNotUnderstand:arguments:")),
            next_dispatch, universe)
        self._selector = selector

    def execute_mate_dispatch(self, rcvr, args, call_frame, lookup_method):
        if rcvr.get_class(self._universe) == self._expected_class:
            return self._cached_method.invoke(rcvr, [self._selector, self._universe.new_array_from_list(args)], call_frame)
        else:
            return self._next.execute_mate_dispatch(rcvr, args, call_frame, lookup_method)


# FIXME
# class SuperMateDispatchNode(_AbstractMateDispatchNode):

#     _immutable_fields_ = ['_cached_method']

#     def __init__(self, selector, lookup_method, universe):
#         _AbstractMateDispatchNode.__init__(self, universe)
#         self._cached_method = lookup_class.lookup_invokable(selector)
#         if self._cached_method is None:
#             raise RuntimeError("#dnu support for super missing")

#     def execute_mate_dispatch(self, rcvr, args, call_frame):
#         return self._cached_method.invoke(rcvr, args, call_frame)

#     def _accept(self, visitor):
#         visitor.visit_SuperDispatchNode(self)
