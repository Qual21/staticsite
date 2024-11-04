from textnode import *
from htmlnode import *
from blocks import *
from nodes import *
import re
import os
import shutil

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

def main():
    script_dir = os.path.dirname(__file__)  # gets the src directory
    project_root = os.path.dirname(script_dir)  # gets the parent (root) directory
    static_dir = os.path.join(project_root, "static")
    public_dir = os.path.join(project_root, "public")    

    clean_and_move_folders(static_dir, public_dir)

if __name__ == "__main__":
    main()
