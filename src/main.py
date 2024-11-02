from textnode import *
from htmlnode import *


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT.value:
        #This should become a LeafNode with no tag, just a raw text value.
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD.value:
        #This should become a LeafNode with a "b" tag and the text
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC.value:
        #"i" tag, text
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE.value:
        #"code" tag, text
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK.value:
        #"a" tag, anchor text, and "href" prop
        return LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
    elif text_node.text_type == TextType.IMAGE.value:
        #"img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    else:
        #error
        raise ValueError("Unsupported text type")

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
