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
                **{
                    "href": text_node.url
                }
                )
        
        case TextType.IMAGE:
            return LeafNode(
                "img",
                " ",
                **{
                    "src": text_node.url,
                    "alt": text_node.text
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

        if cleaned:
            for cleansed in cleaned:
                final_result.append(TextNode(cleansed, TextType.NORMAL))
                if match_queue:
                    alt, url = match_queue.popleft()
                    final_result.append(TextNode(alt, TextType.IMAGE, url))
        else:
            alt, url = match_queue.popleft()
            final_result.append(TextNode(alt, TextType.IMAGE, url))
        return final_result
    
    result = []
    if len(old_nodes) > 1:
        for node in old_nodes:
            result.append(main_job(node.text)) if has_image(node) else result.append(node)
        return result
    elif len(old_nodes) == 1:
        single_list = main_job(old_nodes[0].text)
        return single_list[0] if has_image(old_nodes[0]) else [old_nodes[0]] 
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
        for links in matches:
            match_queue.append(links)

        if cleaned:
            for cleansed in cleaned:
                final_result.append(TextNode(cleansed, TextType.NORMAL))
                if match_queue:
                    alt, url = match_queue.popleft()
                    final_result.append(TextNode(alt, TextType.LINK, url))
        else:
            alt, url = match_queue.popleft()
            final_result.append(TextNode(alt, TextType.LINK, url))
        return final_result
    
    result = []
    if len(old_nodes) > 1:
        for node in old_nodes:
            result.append(main_job(node.text)) if has_link(node) else result.append(node)
        return result
    elif len(old_nodes) == 1:
        single_list = main_job(old_nodes[0].text)
        return single_list if has_link(old_nodes[0]) else [old_nodes[0]] 
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
            img_node = split_nodes_image([node])
            if type(img_node) == list:
                tmp2.extend(split_nodes_image([node]))
            else:
                tmp2.extend([split_nodes_image([node])])
        else: 
            tmp2.extend([node])
        res2.extend(tmp2)

    ### LINK LOOP
    res3 = []
    for node in res2:
        tmp3 = []
        if has_link(node):
            addition = split_nodes_link([node])
            tmp3.append(addition)
        else: 
            tmp3.extend([node])
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
    if block[:2] == "# " or block[:3] == "## " or block[:4] == "### " or block[:5] == "#### " or block[:6] == "##### " or block[:7] == "###### ":
        return BlockType.heading
    elif block[:3] == "```":
        return BlockType.code
    elif block[:2] == "> ":
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
                block_replacement = text_to_textnodes(block.replace('\n', ' '))
                internal_conversion = []
                if isinstance(block_replacement[0], list):
                    for blockr in block_replacement[0]:
                        conversion = text_node_to_html_node(blockr) if isinstance(blockr, TextNode) else text_node_to_html_node(blockr[0])
                        internal_conversion.append(conversion)
                else:
                    for blockr in block_replacement:
                        conversion = text_node_to_html_node(blockr) if isinstance(blockr, TextNode) else text_node_to_html_node(blockr[0])
                        internal_conversion.append(conversion)
                res.append(ParentNode('p', internal_conversion))
            case BlockType.heading:
                heading_level = count_sharp_symbol(block)
                block = block.replace("#","")
                block = block.strip()
                value = list(map(lambda x: list(map(lambda y: text_node_to_html_node(y),x)) if isinstance(x, list) else text_node_to_html_node(x), text_to_textnodes(block.replace('\n', ' '))))
                res.append(ParentNode(f'h{heading_level}', value[0] if isinstance(value[0], list) else value))
            case BlockType.quote:
                block_splits = block.split('\n')
                cleaned_list = list(map(lambda x: x.replace(">", ""), block_splits))
                super_clean = []
                for element in cleaned_list:
                    if not element:
                        continue
                    else:
                        super_clean.append(element)
                text_to_text_node_list = list(map(lambda x: text_to_textnodes(x), super_clean))
                for list_node in text_to_text_node_list:
                    res.append(LeafNode('blockquote', list_node[0].text.strip()))
            case BlockType.code:
                res.append(ParentNode('pre',[LeafNode('code', block.replace("```", ""))]))
            case BlockType.unordered_list:
                list_res = []
                splits = block.split('\n')
                i = 1
                for split in splits:
                    split = clean_unordered_split(split)
                    list_of_childs = list(map(lambda x: list(map(lambda y: text_node_to_html_node(y),x)) if isinstance(x, list) else text_node_to_html_node(x), text_to_textnodes(split)))
                    list_node = ParentNode('li', list_of_childs[0] if isinstance(list_of_childs[0], list) else list_of_childs)
                    list_res.append(list_node)
                res.append(ParentNode('ul', list_res))    
            case BlockType.ordered_list:
                list_res = []
                splits = block.split('\n')
                i = 1
                for split in splits:
                    split = clean_ordered_split(split)
                    list_of_childs = list(map(lambda x: list(map(lambda y: text_node_to_html_node(y),x)) if isinstance(x, list) else text_node_to_html_node(x), text_to_textnodes(split)))
                    list_node = ParentNode('li', list_of_childs[0] if isinstance(list_of_childs[0], list) else list_of_childs)
                    list_res.append(list_node)
                res.append(ParentNode('ol', list_res))
    return ParentNode('div', res)

def clean_ordered_split(split):
    split = re.sub(r"\d{1}. ", "", split)
    return split

def clean_unordered_split(split):
    split = re.sub(r"- ", "", split)
    return split
        
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
        return title
    else:
        raise Exception("your file needs a title")
    
def count_sharp_symbol(block):
    count = 0
    for c in block:
        if c == "#":
            count += 1
    return count
def generate_page(from_path, template_path, dest_path):
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as source_file:
        md_file = source_file.read()

    title = extract_title(md_file)
    title = title.replace("#", "")
    title = title.strip()
    md_object_file = markdown_to_html_node(md_file)

    html_file = md_object_file.to_html()
    print(f"----Printing HTML: {html_file}")
    with open(template_path) as template_file:
        loaded_template_file = template_file.read()

    # These two lines were not updating the string — remember strings are immutable
    loaded_template_file = loaded_template_file.replace('{{ Title }}', title)
    loaded_template_file = loaded_template_file.replace('{{ Content }}', html_file)

    with open(dest_path, 'w') as target_file:
        target_file.write(loaded_template_file)
        
