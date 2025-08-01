from textnode import TextNode, TextType
from copystatic import copy_static_files
import os
import shutil
from markdown_blocks import markdown_to_html_node
from gennpages import generate_page, generate_pages_recursive
import sys

dir_path_static = "./static"
dir_path_public = "./docs"
default_basepath = "/"
dir_path_content = "./content"
template_path = "./template.html"
        

def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_static_files(dir_path_static, dir_path_public)

    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)


if __name__ == "__main__":
    main()