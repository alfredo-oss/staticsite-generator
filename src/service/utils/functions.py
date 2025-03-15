from service.nodes.textnode import TextNode, TextType
from service.nodes.leafnode import LeafNode
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
        for c in node.text:
            s += c
            if delimiter == c:
                count += 1
                s.replace(delimiter, "")
        if count == 2:
            return True
        else:
            return False
        
    # how do i know which part of the splitted array will be the one that has to be assigned with the special delimiter type?
    res = []
    for old_node in old_nodes:
        aux = []
        if has_matching_delimiter(old_node, delimiter):
            text_first, dif_text, text_second = old_node.text.split(delimiter)
            aux.append(TextNode(text_first, TextType.NORMAL))
            aux.append(TextNode(dif_text, text_type))
            aux.append(TextNode(text_second, TextType.NORMAL)) 
        res.extend(aux)
    return res

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
            print(f"TextNode({cleansed}, TextType.NORMAL)")
            if match_queue:
                alt, url = match_queue.popleft()
                final_result.append(TextNode(alt, TextType.IMAGE, url))
                print(f"TextNode({alt}, TextType.IMAGE, {url})")
        return final_result
    
    result = []
    if len(old_nodes) > 1:
        for node in old_nodes:
            result.append(main_job(node.text))
        return result
    elif len(old_nodes) == 1:
        return main_job(old_nodes[0].text)
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
            print(f"TextNode({cleansed}, TextType.NORMAL)")
            if match_queue:
                alt, url = match_queue.popleft()
                final_result.append(TextNode(alt, TextType.LINK, url))
                print(f"TextNode({alt}, TextType.IMAGE, {url})")
        return final_result
    
    result = []
    if len(old_nodes) > 1:
        for node in old_nodes:
            result.append(main_job(node.text))
        return result
    elif len(old_nodes) == 1:
        return main_job(old_nodes[0].text)
    else:
        return result
