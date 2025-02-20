from enum import Enum

class TextType(Enum):
    NORMAL = "NORMAL"
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    CODE = "CODE"
    LINK = "LINK"
    IMAGE = "IMAGE"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node) -> bool:
        return ((self.text == node.text) and
                (self.text_type == node.text_type) and
                (self.url == node.url))
    
    def __repr__(self):
        return f"TextNode{self.text, self.text_type, self.url}"