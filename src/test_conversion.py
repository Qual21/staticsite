import unittest
from textnode import *
from htmlnode import *
from main import *

class TestTextNodeToHtmlNode(unittest.TestCase):
    
    def test_text_node_plain_text(self):
        text_node = TextNode("Hello, world!", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), "Hello, world!")

    def test_text_node_bold_text(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_text_node_italic_text(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_text_node_code_text(self):
        text_node = TextNode("Code snippet", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), "<code>Code snippet</code>")

    def test_text_node_link_text(self):
        text_node = TextNode("OpenAI", TextType.LINK, url="https://openai.com")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), '<a href="https://openai.com">OpenAI</a>')

    def test_text_node_image(self):
        text_node = TextNode("Image description", TextType.IMAGE, url="https://example.com/image.jpg")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), '<img src="https://example.com/image.jpg" alt="Image description"></img>')

    def test_unsupported_text_type(self):
        with self.assertRaises(TypeError):
            text_node_to_html_node(TextNode("Unsupported text", "unsupported"))

class TestSplitNodesImage(unittest.TestCase):

    def test_single_image(self):
        # Single image in the text
        node = TextNode(
            "Here is an image ![rick roll](https://i.imgur.com/aKaOqIh.gif)",
            TextType.TEXT
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif")
        ]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        # Text with multiple images
        node = TextNode(
            "Text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and another image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("Text with an image ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and another image ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertEqual(result, expected)

    def test_text_only(self):
        # No images in the text
        node = TextNode("This is just plain text without images.", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("This is just plain text without images.", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_empty_text(self):
        # Empty text input
        node = TextNode("", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_image_only(self):
        # Text containing only an image
        node = TextNode("![solo image](https://i.imgur.com/solo.png)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("solo image", TextType.IMAGE, "https://i.imgur.com/solo.png")
        ]
        self.assertEqual(result, expected)

class TestSplitNodesLink(unittest.TestCase):

    def test_single_link(self):
        # Single link in the text
        node = TextNode("This is a link to [Google](https://www.google.com)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("This is a link to ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://www.google.com")
        ]
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        # Text with multiple links
        node = TextNode("Link to [Google](https://www.google.com) and [YouTube](https://www.youtube.com)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Link to ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://www.google.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("YouTube", TextType.LINK, "https://www.youtube.com")
        ]
        self.assertEqual(result, expected)

    def test_text_only(self):
        # No links in the text
        node = TextNode("This is just plain text without links.", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("This is just plain text without links.", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_empty_text(self):
        # Empty text input
        node = TextNode("", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_link_only(self):
        # Text containing only a link
        node = TextNode("[GitHub](https://www.github.com)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("GitHub", TextType.LINK, "https://www.github.com")
        ]
        self.assertEqual(result, expected)

    def test_mixed_content_with_multiple_links(self):
        # Complex text with multiple links and surrounding text
        node = TextNode(
            "Here is [GitHub](https://www.github.com), and also [Boot.dev](https://www.boot.dev) and more text.",
            TextType.TEXT
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("Here is ", TextType.TEXT),
            TextNode("GitHub", TextType.LINK, "https://www.github.com"),
            TextNode(", and also ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and more text.", TextType.TEXT)
        ]
        self.assertEqual(result, expected)





if __name__ == "__main__":
    unittest.main()