from .htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, **kwargs):
        super().__init__(tag, value, **kwargs)


    def to_html(self):
        print(self.tag)
        print(self.value)
        if not self.value:
            raise ValueError()
        elif not self.tag:
            return self.value
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'