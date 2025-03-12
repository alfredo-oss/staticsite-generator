from service.nodes.textnode import TextNode, TextType
from service.nodes.leafnode import LeafNode

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
            print(c)
            s += c
            if delimiter == c:
                count += 1
                s.replace(delimiter, "")
        print(count)
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
    print(res)
    return res