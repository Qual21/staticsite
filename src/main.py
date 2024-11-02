from textnode import *
from htmlnode import *


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT.value:                                         #plain text
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD.value:                                       #bold
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC.value:                                     #italic
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE.value:                                       #code
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK.value:                                       #link
        return LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
    elif text_node.text_type == TextType.IMAGE.value:                                      #image
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError("Unsupported text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not isinstance(old_nodes, list):
        old_nodes = [old_nodes]
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
            continue
        
        parts = node.text.split(delimiter)

        if len(parts) == 1:
            new_nodes.append(node)
            continue
        for i, part in enumerate(parts):
            if not (i & 1):     # Even
                if part:  # Only create node if part is not empty
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:               # Odd 
                if part:  # Only create node if part is not empty
                    new_nodes.append(TextNode(part, text_type))    

    return new_nodes    




def main():
    test_nodes = [
        TextNode("Regular text", TextType.TEXT),
        TextNode("Bold text", TextType.BOLD),
        TextNode("Italic text", TextType.ITALIC),
        TextNode("Code block", TextType.CODE),
        TextNode("Link text", TextType.LINK, "https://example.com"),
        TextNode("Image description", TextType.IMAGE, "https://example.com/image.jpg")
    ]
    
    for node in test_nodes:
        try:
            html_node = text_node_to_html_node(node)
            print(f"Input: {node}")
            print(f"Output HTML: {html_node.to_html()}\n")
        except Exception as e:
            print(f"Error converting node {node}: {str(e)}\n")
    

if __name__ == "__main__":
    main()
