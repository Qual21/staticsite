import unittest

from htmlnode import *

test_dict = {'key0': 'value0', 'key1': 'value1', 'key2': 'value2'}
class TestHTMLNode(unittest.TestCase):
    
    def test_eq(self):
        node = HTMLNode(tag="This is a different text node", value="hbu")
        node2 = HTMLNode(tag="This is a different text node", value="hbu")
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = HTMLNode(tag="This is a different text node", props=test_dict)
        node2 = HTMLNode(tag="This is a different text node", props=test_dict)
        self.assertEqual(node, node2)

    def test_eq3(self):
        node = HTMLNode(tag="This is a text node")
        node2 = HTMLNode(value="This is a cvstext node")
        self.assertNotEqual(node, node2)
### leaf tests
    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
### parent tests
    def test_parent_node_with_children(self):
        child1 = LeafNode("span", "Hello")
        child2 = LeafNode("span", "World", props={"class": "highlight"})
        parent = ParentNode("div", children=[child1, child2], props={"id": "container"})
        
        expected_html = '<div id="container"><span>Hello</span><span class="highlight">World</span></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_parent_node_nested_children(self):
        inner_child = LeafNode("i", "Nested")
        inner_parent = ParentNode("p", children=[inner_child], props={"class": "inner"})
        outer_parent = ParentNode("div", children=[inner_parent])
        
        expected_html = '<div><p class="inner"><i>Nested</i></p></div>'
        self.assertEqual(outer_parent.to_html(), expected_html)

    def test_parent_node_with_no_tag(self):
        child = LeafNode("span", "Hello")
        with self.assertRaises(ValueError):
            ParentNode(None, children=[child]).to_html()

    def test_parent_node_with_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", children=[]).to_html()

    def test_parent_node_with_props_only(self):
        child = LeafNode("span", "Only child")
        parent = ParentNode("section", children=[child], props={"data-type": "example"})
        
        expected_html = '<section data-type="example"><span>Only child</span></section>'
        self.assertEqual(parent.to_html(), expected_html)


if __name__ == "__main__":
    unittest.main()