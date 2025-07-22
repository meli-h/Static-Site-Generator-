import unittest

from htmlnode import HTMLNode , LeafNode , ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag="div", props={"class": "container", "id": "main"})
        expected = 'class="container" id="main"'
        self.assertEqual(node.props_to_html(), expected)
    def test_repr(self):
        node = HTMLNode(tag="div", props={"class": "container", "id": "main"})
        
        expected = repr(node)
        self.assertEqual(expected, f"HTMLNode(tag={node.tag}, value={node.value}, children={node.children}, props={node.props})")

    def test_no_props(self):
        node = HTMLNode(tag="span")
        self.assertEqual(node.props_to_html(), "")

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode(tag="p", value="Hello, World!", props={"class": "text"})
        expected = '<p class="text">Hello, World!</p>'
        self.assertEqual(node.to_html(), expected)

    def test_no_tag(self):
        node = LeafNode(None ,value="Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    
class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_no_children(self):
       
        with self.assertRaises(ValueError) as ctx:
            
            ParentNode(tag="div", children=None).to_html()

        
        self.assertEqual(
            str(ctx.exception),
            "ParentNode requires at least one child node"
        )
    def test_no_tag(self):
        with self.assertRaises(ValueError) as ctx:
            ParentNode(tag=None, children=[LeafNode("p", "Hello")]).to_html()
        
        self.assertEqual(
            str(ctx.exception),
            "ParentNode must have a tag"
        )