from textnode import *
from htmlnode import *
from blocks import *
from nodes import *
from pathlib import Path
import re
import os
import shutil

script_dir = os.path.dirname(__file__)  # gets the src directory
project_root = os.path.dirname(script_dir)  # gets the parent (root) directory
static_dir = os.path.join(project_root, "static")
public_dir = os.path.join(project_root, "public")    


def clean_and_move_folders(sender, receiver):
    if not os.path.exists(sender):
        raise ValueError("No sender directory")
    
    if os.path.exists(receiver):
        shutil.rmtree(receiver)  # Remove all contents in receiving folder
    os.makedirs(receiver, exist_ok=True)

    recursive_copy(sender, receiver)


def recursive_copy(current_sender, current_receiver):
    for item in os.listdir(current_sender):
        source_path = os.path.join(current_sender, item)
        target_path = os.path.join(current_receiver, item)

        if os.path.isdir(source_path): # Create the corresponding directory in the receiver and recurse
            os.makedirs(target_path, exist_ok=True)
            recursive_copy(source_path, target_path)
        else: # If it's a file, copy it directly to the receiver
            print(shutil.copy2(source_path, target_path))
            shutil.copy2(source_path, target_path)

def extract_title(markdown):
    pass

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    file_path = os.path.join(project_root, from_path)   ## "content/index.md"
    templ_path = os.path.join(project_root, template_path)
    dest_full_path = os.path.join(project_root, dest_path)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            html_string = (markdown_to_html_node(content))
    except FileNotFoundError:
        print(f'File "{file_path}" not found.')
        return

    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            template = file.read()
    except FileNotFoundError:
        print(f'File "{file_path}" not found.')
        return

    title_match = re.search(r'<h1>(.*?)</h1>', html_string)
    if title_match:
        title = title_match.group(1)  # Get the text between <h1> tags
    else:
        title = "Untitled"

    final_html = template.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_string)

    os.makedirs(os.path.dirname(dest_full_path), exist_ok=True)

    try:
        with open(dest_full_path, 'w', encoding='utf-8') as file:
            file.write(final_html)
        print(f"Successfully generated {dest_full_path}")
    except Exception as e:
        print(f"Error writing to {dest_full_path}: {str(e)}")


def generate_all_pages(content_dir, template_path, dest_dir):

    content_root = os.path.join(project_root, content_dir)
    
    for root, _, files in os.walk(content_root):                         # Walk through all files and directories
        for file in files:
            if file.endswith('.md'):
                rel_path = os.path.relpath(root, content_root)
                if rel_path == '.':
                    from_path = os.path.join(content_dir, file)
                else:
                    from_path = os.path.join(content_dir, rel_path, file)
                
                # Construct destination path, replacing .md with .html
                dest_path = os.path.join(
                    dest_dir,
                    rel_path,
                    file.replace('.md', '.html')
                )
                
                # Generate the page
                print(f"\nProcessing {from_path}")
                generate_page(from_path, template_path, dest_path)

def main():



    test_blocks = """
#This is the header block

##This is the second header block

>This is
>a quote
>block

"""
    #print(markdown_to_html_node(test_blocks))

    clean_and_move_folders(static_dir, public_dir)
    generate_all_pages(
        "content",
        "template.html",
        "public"
    )

if __name__ == "__main__":
    main()
