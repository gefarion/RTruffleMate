import unittest
from rtruffle.node import Node


class VisitorTest(unittest.TestCase):

    def test_visit_child(self):
        child = ChildNode("a")
        visitor = NodeVisitor()
        child.accept(visitor)

        self.assertEqual("a", visitor._values)

    def test_visit_root(self):
        root_node = RootNode(value="b")
        visitor = NodeVisitor()
        root_node.accept(visitor)

        self.assertEqual("b", visitor._values)

    def test_visit_root_with_one_child(self):
        child = ChildNode("b")
        root_node = RootNode(child_node1=child, value="a")
        visitor = NodeVisitor()
        root_node.accept(visitor)

        self.assertEqual("ab", visitor._values)

    def test_visit_root_with_two_child(self):
        child1 = ChildNode("b")
        child2 = ChildNode("c")
        root_node = RootNode(child_node1=child1, child_node2=child2, value="a")
        visitor = NodeVisitor()
        root_node.accept(visitor)

        self.assertEqual("abc", visitor._values)

    def test_visit_root_with_child_list(self):
        child1 = ChildNode("b")
        child2 = ChildNode("c")
        child3 = ChildNode("d")
        root_node = RootNodeWithChildList([child1, child2, child3], "a")

        visitor = NodeVisitor()
        root_node.accept(visitor)

        self.assertEqual("abcd", visitor._values)


class RootNode(Node):

    _child_nodes_ = ['_child_node1', '_child_node2']

    def __init__(self, child_node1 = None, child_node2 = None, value = None):
        Node.__init__(self)
        self._child_node1 = self.adopt_child(child_node1)
        self._child_node2 = self.adopt_child(child_node2)
        self._value = value


class RootNodeWithChildList(Node):

    _child_nodes_ = ['_child_nodes[*]']

    def __init__(self, child_nodes = None, value = None):
        Node.__init__(self)
        assert isinstance(child_nodes, list)
        self._child_nodes = self.adopt_children(child_nodes)
        self._value = value

class ChildNode(Node):
    def __init__(self, value):
        Node.__init__(self)
        self._value = value

class NodeVisitor:
    def __init__(self):
        self._values = ""

    def visitChildNode(self, node):
        self._values += node._value
        return True

    def visitRootNode(self, node):
        self._values += node._value
        return True


    def visitRootNodeWithChildList(self, node):
        self._values += node._value
        return True
