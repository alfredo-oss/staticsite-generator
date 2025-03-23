from typing import Optional
from .htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], **kwargs: Optional[dict]):
        super().__init__(tag, None, children, **kwargs)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("tag is required")
        elif not self.children:
            raise ValueError("parent nodes need to have children associated")
        else:
            s = ""
            for child in self.children:
                s += f"{child.to_html()}"
            s = f"<{self.tag}>" + s + f"</{self.tag}>"
            return s