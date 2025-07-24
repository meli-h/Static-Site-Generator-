from textnode import TextNode , TextType
from link_extractor import extract_markdown_links, extract_markdown_images


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type == text_type.TEXT:
            parts = old_node.text.split(delimiter)    
            for index, part in enumerate(parts):
                if index % 2 == 0:
                     new_nodes.append(TextNode(part, text_type.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type.BOLD))
        else:
            new_nodes.append(old_node)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
           
            images = extract_markdown_images(old_node.text)
            if not images:
                new_nodes.append(old_node)
                continue
                
           
            remaining_text = old_node.text
            
          
            for alt_text, url in images:
                
                image_markdown = f"![{alt_text}]({url})"
                
                parts = remaining_text.split(image_markdown, 1)
                
                
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                
                
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                
                remaining_text = parts[1] if len(parts) > 1 else ""
            
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
        else:
            new_nodes.append(old_node)
    
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            
            links = extract_markdown_links(old_node.text)
            if not links:
                new_nodes.append(old_node)
                continue
                
            remaining_text = old_node.text
            
            
            for link_text, url in links:
                link_markdown = f"[{link_text}]({url})"
                
                
                parts = remaining_text.split(link_markdown, 1)
                
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                
                
                new_nodes.append(TextNode(link_text, TextType.LINK, url))
                
                remaining_text = parts[1] if len(parts) > 1 else ""
            
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
        else:
            new_nodes.append(old_node)
    
    return new_nodes
    
