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

res = [text]

for delimiter, delimiter_type in delimiters:
    tmp = []
    for text_element in res:
        #print(text_element)
        #print(delimiter, delimiter_type)
        tmp_txt_node = TextNode(text_element, TextType.NORMAL)
        tmp = split_nodes_delimiter([tmp_txt_node], delimiter, delimiter_type)
        print(tmp)
        #print(split_nodes_delimiter([TextNode(text_element, TextType.NORMAL)]))
     

#print(res)