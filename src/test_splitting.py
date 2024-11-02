import unittest
from textnode import *
from htmlnode import *
from main import *


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
    test_split_nodes()
