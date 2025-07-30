from textnode import TextNode, TextType
from copystatic import copy_static_files
import os
import shutil
from markdown_blocks import markdown_to_html_node
from gennpages import generate_page, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"


        

def main():

    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_static_files(dir_path_static, dir_path_public)

    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()