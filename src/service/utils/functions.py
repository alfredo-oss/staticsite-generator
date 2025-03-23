from service.nodes.textnode import TextNode, TextType
from service.nodes.leafnode import LeafNode
from service.blocks.block_types import BlockType
from service.nodes.parentnode import ParentNode
from collections import deque
import re
import os
import shutil

def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(
                None, 
                text_node.text
                )
        
        case TextType.BOLD:
            return LeafNode(
                "b",
                text_node.text
                )
        
        case TextType.ITALIC:
            return LeafNode(
                "i",
                text_node.text
                )
        
        case TextType.CODE:
            return LeafNode(
                "code", 
                text_node.text
                )
        
        case TextType.LINK:
            return LeafNode(
                "a",
                text_node.text,
                {"href":text_node.url}
                )
        
        case TextType.IMAGE:
            return LeafNode(
                "img",
                "",
                {
                    "src":text_node.url,
                    "alt":text_node.text
                }
                )
        
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list:
    def has_matching_delimiter(node: TextNode, delimiter: str) -> bool:
        s = ""
        count = 0
        if len(delimiter) == 1:
            for c in node.text:
                s += c
                if delimiter == c:
                    count += 1
                    s.replace(delimiter, "")
            if count == 2:
                return True
            else:
                return False
        if len(delimiter) == 2:
            j = 0
            for i in range(1, len(node.text)):
                if delimiter == (node.text[i] + node.text[j]):
                    count += 1
                j += 1
            if count == 2:
                return True
            else:
                return False            
        
    
    res = []
    for old_node in old_nodes:
        aux = []
        if has_matching_delimiter(old_node, delimiter):
            text_first, dif_text, text_second = old_node.text.split(delimiter)
            aux.append(TextNode(text_first, TextType.NORMAL))
            aux.append(TextNode(dif_text, text_type))
            aux.append(TextNode(text_second, TextType.NORMAL)) 
        else:
            aux.append(old_node)
        res.extend(aux)
    return res 

def has_image(node):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", node.text)
    return True if matches else False

def has_link(node):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", node.text)
    return True if matches else False

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    def main_job(text):
        final_result = []
        matches = extract_markdown_images(text)
        res = [text]

        delimiters = []
        for image_alt, image_url in matches:
            delimiters.append(f"![{image_alt}]({image_url})")

        for delimiter in delimiters:
            tmp = []
            for text_element in res:
                tmp.extend(text_element.split(delimiter))
            res=tmp


        cleaned = []
        for element in res:
            if element == "":
                continue
            else:
                cleaned.append(element)

        match_queue = deque()
        for imgs in matches:
            match_queue.append(imgs)

        for cleansed in cleaned:
            final_result.append(TextNode(cleansed, TextType.NORMAL))
            if match_queue:
                alt, url = match_queue.popleft()
                final_result.append(TextNode(alt, TextType.IMAGE, url))
        return final_result
    
    result = []
    if len(old_nodes) > 1:
        for node in old_nodes:
            result.append(main_job(node.text)) if has_image(node) else result.append(node)
        return result
    elif len(old_nodes) == 1:
        return main_job(old_nodes[0].text) if has_image(old_nodes[0]) else [old_nodes[0]] 
    else:
        return result

def split_nodes_link(old_nodes):
    def main_job(text):
        final_result = []
        matches = extract_markdown_links(text)
        res = [text]

        delimiters = []
        for link_alt, link_url in matches:
            delimiters.append(f"[{link_alt}]({link_url})")

        for delimiter in delimiters:
            tmp = []
            for text_element in res:
                tmp.extend(text_element.split(delimiter))
            res=tmp


        cleaned = []
        for element in res:
            if element == "":
                continue
            else:
                cleaned.append(element)

        match_queue = deque()
        for imgs in matches:
            match_queue.append(imgs)

        for cleansed in cleaned:
            final_result.append(TextNode(cleansed, TextType.NORMAL))
            if match_queue:
                alt, url = match_queue.popleft()
                final_result.append(TextNode(alt, TextType.LINK, url))
        return final_result
    
    result = []
    if len(old_nodes) > 1:
        for node in old_nodes:
            result.append(main_job(node.text)) if has_link(node) else result.append(node)
        return result
    elif len(old_nodes) == 1:
        return main_job(old_nodes[0].text) if has_link(old_nodes[0]) else [old_nodes[0]] 
    else:
        return result
    
def text_to_textnodes(text):
    res = [TextNode(text, TextType.NORMAL)]
    delimiters = [("**", TextType.BOLD), ("`", TextType.CODE), ("_", TextType.ITALIC)]
    ### TEXT LOOP

    for delimiter, delimiter_type in delimiters:
        tmp = []
        for text_element in res:
            tmp.extend(split_nodes_delimiter([text_element], delimiter, delimiter_type))
        res = tmp

    ### IMAGE LOOP

    res2 = []
    for node in res:
        tmp2 = []
        if node.text_type == TextType.NORMAL:
            tmp2.extend(split_nodes_image([node]))
        else: 
            tmp2.append(node)
        res2.extend(tmp2)

    ### LINK LOOP

    res3 = []
    for node in res2:
        tmp3 = []
        if node.text_type == TextType.NORMAL:
            tmp3.extend(split_nodes_link([node]))
        else: 
            tmp3.append(node)
        res3.extend(tmp3)
    return res3

def markdown_to_blocks(markdown):
    splits  = markdown.split("\n\n")
    splits = list(map(lambda x: x.strip(), splits))
    res = []
    for element in splits:
        if element:
            res.append(element)
        else:
            continue
    return res

def block_to_block(block) -> BlockType:
    if block[0] == "#":
        return BlockType.heading
    elif block[:3] == "```":
        return BlockType.code
    elif block[0] == ">":
        return BlockType.quote
    elif block[0] == "-":
        return BlockType.unordered_list
    elif block[0].isdigit() and block[1] == ".":
        return BlockType.ordered_list
    else:
        return BlockType.paragraph
    
def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    res = []
    for block in md_blocks:
        match block_to_block(block):
            case BlockType.paragraph:
                res.append(ParentNode('p', list(map(lambda y: text_node_to_html_node(y), text_to_textnodes(block.replace('\n', ' '))))))
            case BlockType.heading:
                res.append(ParentNode('h1', list(map(lambda y: text_node_to_html_node(y), text_to_textnodes(block.replace('\n', ' '))))))
            case BlockType.code:
                res.append(ParentNode('pre',[LeafNode('code', block.replace("```", ""))]))
            case BlockType.quote:
                res.append(ParentNode('blockquote', list(map(lambda y: text_node_to_html_node(y), text_to_textnodes(block.replace('\n', ' '))))))
            case BlockType.unordered_list:
                res.append(ParentNode('ul', list(map(lambda y: text_node_to_html_node(y), text_to_textnodes(block.replace('\n', ' '))))))
            case BlockType.ordered_list:
                res.append(ParentNode('ol', list(map(lambda y: text_node_to_html_node(y), text_to_textnodes(block.replace('\n', ' '))))))
    return ParentNode('div', res)

def copy_resources_recursively(target_path: str, destination_path: str):

    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)

    os.mkdir(destination_path)

    recursive_paths = os.listdir(target_path)

    paths_to_copy = []
    def recursive_copy(source_path, recursive_paths):
        nonlocal target_path
        nonlocal destination_path
        for path in recursive_paths:
            objective_path = source_path + "/" + path
            if os.path.isfile(objective_path):
                paths_to_copy.append(objective_path)
                return
            else:
                os.mkdir(objective_path.replace(target_path, destination_path))
                recursive_copy(objective_path, os.listdir(objective_path))

    recursive_copy(target_path, recursive_paths)

    for path_to_copy in paths_to_copy:
        shutil.copy(path_to_copy, path_to_copy.replace(target_path, destination_path))

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    if "# " in blocks[0]:
        title = blocks[0]
        return title.replace('# ', '')
    else:
        raise Exception("your file needs a title")
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as source_file:
        md_file = source_file.read()
    print(md_file)
    #html_file = markdown_to_html_node(md_file).to_html()
    #title = extract_title(md_file)

    with open(template_path) as template_file:
        loaded_template_file = template_file.read()
    print(loaded_template_file)