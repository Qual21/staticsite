import unittest
from textnode import *
from htmlnode import *
from main import *

class TestInlineMarkdown(unittest.TestCase):
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
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
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

def test_split_nodes():
    # Test case 1: Basic split
    nodes = [TextNode("One **Two** Three", TextType.TEXT)]
    result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    expected = [
        TextNode("One ", TextType.TEXT),
        TextNode("Two", TextType.BOLD),
        TextNode(" Three", TextType.TEXT)
    ]
    print(result)
    print("Test 1 passed:", result == expected)
    
    # Test case 2: Multiple delimiters
    nodes = [TextNode("One **Two** Three **Four**", TextType.TEXT)]
    result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    expected = [
        TextNode("One ", TextType.TEXT),
        TextNode("Two", TextType.BOLD),
        TextNode(" Three ", TextType.TEXT),
        TextNode("Four", TextType.BOLD)
    ]
    print("Test 2 passed:", result == expected)
    
    # Test case 3: No delimiters
    nodes = [TextNode("Plain text", TextType.TEXT)]
    result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    expected = [TextNode("Plain text", TextType.TEXT)]
    print("Test 3 passed:", result == expected)
    
    # Test case 4: Empty text between delimiters
    nodes = [TextNode("One **** Three", TextType.TEXT)]
    result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    expected = [
        TextNode("One ", TextType.TEXT),
        TextNode(" Three", TextType.TEXT)
    ]
    print("Test 4 passed:", result == expected)

if __name__ == "__main__":
    test_split_nodes() #own tests
    unittest.main() #boot tests
