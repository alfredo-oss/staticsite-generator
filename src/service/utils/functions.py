from service.nodes.textnode import TextNode, TextType
from service.nodes.leafnode import LeafNode
from service.blocks.block_types import BlockType
from collections import deque
import re

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
    ol_exp = re.compile(r"\d{1}.")
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