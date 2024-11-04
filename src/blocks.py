from textnode import *
from htmlnode import *
from main import *
from nodes import *
import re

def markdown_to_blocks(markdown):
    blocks = markdown.strip().split('\n\n')
    return [block.strip() for block in blocks if block.strip()]

def block_to_block_type(block):
    block = block.strip()
    
    if not block:
        return "empty block"
    

    if block.startswith("#"):
        return "heading"
    elif block.startswith("```") and block.endswith("```"):
        return "code"
    elif all(line.startswith('>') for line in block.splitlines() if line.strip()):
        return "quote"
    elif all((line.startswith('- ') or line.startswith('* '))
             for line in block.splitlines() if line.strip()):
        return "unordered_list"
    #elif all(re.match(r"^\d+\. ", line)for line in block.splitlines() if line.strip()):
    #    return "ordered list"           #numbered, not caring for order
    
    lines = block.splitlines()
    expected_number = 1
    is_ordered = True

    for line in lines:
        line = line.strip()
        if line: 
            match = re.match(r"^(\d+)\. ", line)
            if not match:
                is_ordered = False
                break
            number = int(match.group(1))
            if number != expected_number:
                is_ordered = False
                break
            expected_number += 1
    
    if is_ordered:
        return "ordered_list"
    
    
    return "normal_paragraph"

def markdown_to_html_node(markdown):

    blocks = markdown_to_blocks(markdown)
    new_blocks = []

    for block in blocks:
        nblocks = []
        block_type = block_to_block_type(block)
        lines = block.splitlines()

        if block_type == "unordered_list":
            un_temp = []
            for line in lines:
                l = line.lstrip('*- ')
                tnodes = (text_to_textnodes(l))
                hnodes = []
                for tnode in tnodes:
                    #print(tnode)
                    #print(text_node_to_html_node(tnode).to_html())
                    hnodes.append(text_node_to_html_node(tnode).to_html())
                #print((f"<li>{''.join(hnodes)}</li>"))
                un_temp.append(f"<li>{''.join(hnodes)}</li>")
            #print(f"<ul>{un_temp}</ul>")
            nblocks.append(f"<ul>{''.join(un_temp)}</ul>")

        if block_type == "ordered_list":
            o_temp = []
            for line in lines:
                l = line[2:].strip()
                tnodes = (text_to_textnodes(l))
                hnodes = []                
                for tnode in tnodes:
                    hnodes.append(text_node_to_html_node(tnode).to_html())
                o_temp.append(f"<li>{''.join(hnodes)}</li>")
            nblocks.append(f"<ol>{''.join(o_temp)}</ol>")

        if block_type == "code":                     ### code should not have formatting
            lines = block.strip("```")
        #    c_temp = []
        #    for line in lines:
        #        tnodes = (text_to_textnodes(line))
        #        hnodes = []                
        #        for tnode in tnodes:
        #            hnodes.append(text_node_to_html_node(tnode).to_html())
        #        c_temp.append(f"{''.join(hnodes)}")
            nblocks.append(f"<pre><code>{lines}</code></pre>")


        if block_type == "quote":
            q_temp = []
            for line in lines:
                l = line.lstrip('> ')
                tnodes = (text_to_textnodes(l))
                hnodes = []                
                for tnode in tnodes:
                    hnodes.append(text_node_to_html_node(tnode).to_html())
                q_temp.append(f"{''.join(hnodes)}")
            nblocks.append(f"<blockquote>{''.join(q_temp)}</blockquote>")

        if block_type == "normal_paragraph":
            plain_temp = []
            for line in lines:
                tnodes = (text_to_textnodes(line))
                hnodes = []                
                for tnode in tnodes:
                    hnodes.append(text_node_to_html_node(tnode).to_html())
                plain_temp.append(f"{''.join(hnodes)}")
            nblocks.append(f"<p>{''.join(plain_temp)}</p>")

        if block_type == "heading":
            hashes = 0
            for char in block:
                if char == "#":
                    hashes += 1
                else:
                    break
            if hashes > 6: hashes = 6
            nblocks.append(f"<h{hashes}>{block[hashes:].strip()}</h{hashes}>")


        new_blocks.append(f"{''.join(nblocks)}")
    


    return ''.join(new_blocks)



#```1. You will rejoice to hear **that** no disaster has accompanied the
#2. commencement of an enterprise which you have regarded with such evil```

test = """
####banana orange car
uhyvgbuhbn

line one **thick** boy
line two *italian* gal

1. Hello, my darling
2. Hello, my ```baby```
3. Hello darkness my old friend """

#print(markdown_to_html_node(test))