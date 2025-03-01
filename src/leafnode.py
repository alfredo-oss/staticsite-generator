from typing import Optional
from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self):
        super().__init__(children=None)

    def to_html(self):
        if not self.value:
            raise ValueError()
        elif not self.tag:
            return self.value
        else:
            return f'<{self.tag}{self.props_to_html()}></{self.tag}>'