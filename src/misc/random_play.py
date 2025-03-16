import re
from service.nodes.textnode import TextNode, TextType
from collections import deque
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
            result.append(main_job(node))
        return result
    elif len(old_nodes) == 1:
        return main_job(old_nodes[0])
    else:
        return result



