import unittest
from markdownsplit import split_nodes_delimiter, split_nodes_image, split_nodes_link
from link_extractor import extract_markdown_images, extract_markdown_links

from textnode import TextNode, TextType
 

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    

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








