import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("Hello", TextType.TEXT)
        expected = f"TextNode({node.text}, {node.text_type.value}, {node.url})"
        self.assertEqual(repr(node), expected)

    def test_url(self):
        node = TextNode("Link", TextType.LINK, "www.example.com")
        self.assertEqual(node.url, "www.example.com")
        self.assertIsNotNone(node.url)

    def test_default_url_is_none(self):
        node = TextNode("No link", TextType.TEXT)
        self.assertIsNone(node.url)
    
    def test_not_eq_different_url(self):
        node1 = TextNode("Image", TextType.IMAGE, url="https://ex.com/a.png")
        node2 = TextNode("Image", TextType.IMAGE, url="https://ex.com/b.png")
        self.assertNotEqual(node1, node2)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

if __name__ == "__main__":
    unittest.main()