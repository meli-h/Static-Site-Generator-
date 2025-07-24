import unittest
from markdownsplit import split_nodes_delimiter, split_nodes_image, split_nodes_link
from link_extractor import extract_markdown_images, extract_markdown_links

from textnode import TextNode, TextType
 

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_with_delimiter(self):
        # When splitting a TEXT node, even parts should be TEXT and odd parts BOLD.
        node = TextNode("hello--world", TextType.TEXT)
        old_nodes = [node]
        delimiter = "--"
        result = split_nodes_delimiter(old_nodes, delimiter, TextType)
        
        expected = [
            TextNode("hello", TextType.TEXT),
            TextNode("world", TextType.BOLD)
        ]
        self.assertEqual(len(result), len(expected))
        for res, exp in zip(result, expected):
            self.assertEqual(res.text, exp.text)
            self.assertEqual(res.text_type, exp.text_type)

    def test_no_split_when_not_text(self):
        # Nodes that are not of TEXT type should remain unchanged.
        node = TextNode("some text", TextType.BOLD)
        old_nodes = [node]
        delimiter = "--"
        result = split_nodes_delimiter(old_nodes, delimiter, TextType)
        self.assertEqual(result, old_nodes)

    def test_multiple_delimiters(self):
        # Test splitting a string that contains several delimiters.
        text = "a--b--c--d"
        node = TextNode(text, TextType.TEXT)
        old_nodes = [node]
        delimiter = "--"
        result = split_nodes_delimiter(old_nodes, delimiter, TextType)
        
        expected = [
            TextNode("a", TextType.TEXT),
            TextNode("b", TextType.BOLD),
            TextNode("c", TextType.TEXT),
            TextNode("d", TextType.BOLD)
        ]
        self.assertEqual(len(result), len(expected))
        for res, exp in zip(result, expected):
            self.assertEqual(res.text, exp.text)
            self.assertEqual(res.text_type, exp.text_type)

    def test_empty_text(self):
        # Splitting an empty string should return a single node with empty text.
        node = TextNode("", TextType.TEXT)
        old_nodes = [node]
        delimiter = "--"
        result = split_nodes_delimiter(old_nodes, delimiter, TextType)
        
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(len(result), len(expected))
        self.assertEqual(result[0].text, expected[0].text)
        self.assertEqual(result[0].text_type, expected[0].text_type)

class TestMarkdownSplit(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_split_nodes_image_single(self):
        # Test single image conversion
        nodes = [
            TextNode("Here is ![alt](url) an image.", TextType.TEXT)
        ]
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode(" an image.", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_image(nodes), expected)

    def test_split_nodes_image_multiple(self):
        # Test multiple images in one node
        nodes = [
            TextNode("![img1](url1) between ![img2](url2)", TextType.TEXT)
        ]
        expected = [
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(" between ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2")
        ]
        self.assertEqual(split_nodes_image(nodes), expected)

    def test_split_nodes_image_no_images(self):
        # Test text without images
        nodes = [
            TextNode("Just plain text", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_image(nodes), nodes)

    def test_split_nodes_image_preserve_other_types(self):
        # Test preservation of non-TEXT nodes
        nodes = [
            TextNode("![img](url)", TextType.TEXT),
            TextNode("bold", TextType.BOLD)
        ]
        expected = [
            TextNode("img", TextType.IMAGE, "url"),
            TextNode("bold", TextType.BOLD)
        ]
        self.assertEqual(split_nodes_image(nodes), expected)

    def test_split_nodes_link_single(self):
        # Test single link conversion
        nodes = [
            TextNode("Here is [text](url) a link.", TextType.TEXT)
        ]
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("text", TextType.LINK, "url"),
            TextNode(" a link.", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_link(nodes), expected)

    def test_split_nodes_link_multiple(self):
        # Test multiple links in one node
        nodes = [
            TextNode("[link1](url1) between [link2](url2)", TextType.TEXT)
        ]
        expected = [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" between ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2")
        ]
        self.assertEqual(split_nodes_link(nodes), expected)

    def test_split_nodes_link_no_links(self):
        # Test text without links
        nodes = [
            TextNode("Just plain text", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_link(nodes), nodes)

    def test_split_nodes_link_preserve_other_types(self):
        # Test preservation of non-TEXT nodes
        nodes = [
            TextNode("[text](url)", TextType.TEXT),
            TextNode("bold", TextType.BOLD)
        ]
        expected = [
            TextNode("text", TextType.LINK, "url"),
            TextNode("bold", TextType.BOLD)
        ]
        self.assertEqual(split_nodes_link(nodes), expected)


    



if __name__ == '__main__':
    unittest.main()








