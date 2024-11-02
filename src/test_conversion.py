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





if __name__ == "__main__":
    unittest.main()