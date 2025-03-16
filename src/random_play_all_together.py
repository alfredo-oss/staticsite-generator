from service.utils.functions import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node
)
from service.nodes.textnode import TextNode, TextType
import re

text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
delimiters = [("**", TextType.BOLD), ("`", TextType.CODE), ("_", TextType.ITALIC)]

res = [TextNode(text,TextType.NORMAL)]

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

print(f"FINAL RESULT: {res3}")


