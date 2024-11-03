from textnode import *
from htmlnode import *
import re



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

def split_nodes_image(old_nodes):
    if not isinstance(old_nodes, list):
        old_nodes = [old_nodes]
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
            continue

        text = node.text
        extracted = extract_markdown_images(node.text)
        #pattern = r"!\[([^\]]+)\]\((http[^\)]+)\)"
        
        if len(extracted) == 0:
            new_nodes.append(node)
            continue

        for extract in extracted:
            sections = text.split(f"![{extract[0]}]({extract[1]})", 1)
            if len(sections) != 2:
                raise ValueError("image not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(extract[0], TextType.IMAGE, extract[1]))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes):
    if not isinstance(old_nodes, list):
        old_nodes = [old_nodes]
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
            continue

        text = node.text
        extracted = extract_markdown_links(node.text)
        #pattern = r"\[([^\]]+)\]\((http[^\)]+)\)"
        
        if len(extracted) == 0:
            new_nodes.append(node)
            continue

        for extract in extracted:
            sections = text.split(f"[{extract[0]}]({extract[1]})", 1)
            if len(sections) != 2:
                raise ValueError("link not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(extract[0], TextType.LINK, extract[1]))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    
    return new_nodes

def text_to_textnodes(text):
    pictured = split_nodes_image(TextNode(text, TextType.TEXT))
    linked = split_nodes_link(pictured)
    bold = split_nodes_delimiter(linked, "**", TextType.BOLD)
    italian = split_nodes_delimiter(bold, "*", TextType.ITALIC)
    coded = split_nodes_delimiter(italian, "`", TextType.CODE)


    return coded



def extract_markdown_images(text):
    pattern = r"!\[([^\]]+)\]\((http[^\)]+)\)"
    matches = re.findall(pattern, text)

    return matches

def extract_markdown_links(text):
    pattern =r"(?<!!)\[([^\]]+)\]\((http[^\)]+)\)"
    matches = re.findall(pattern, text)

    return matches