import os
from markdown_blocks import markdown_to_html_node
from pathlib import Path




def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)

def extract_title(markdown):
    in_code = False
    for line in markdown.splitlines():
        s = line.strip()
        if s.startswith("```") or s.startswith("~~~"):
            in_code = not in_code
            continue
        if not in_code and line.startswith("# "):
            title = line[2:].strip().rstrip("#").strip()
            return title
    raise ValueError("H1 başlık bulunamadı (# ...).")

def generate_page(from_path, template_path, dest_path, basepath):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r', encoding='utf-8') as f:
        markdown = f.read()
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    html_string = markdown_to_html_node(markdown).to_html()

    title = extract_title(markdown)

    new_html = template.replace("{{ Title }}" , title)
    new_html = new_html.replace("{{ Content }}", html_string)  
    new_html = new_html.replace('href="/', 'href="' + basepath)
    new_html = new_html.replace('src="/', 'src="' + basepath)  
    

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(new_html)