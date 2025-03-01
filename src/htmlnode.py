class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, **kwargs):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = kwargs

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self) -> str:
        s = " "
        for key, value in self.props.items():
            s += key.replace("\"", "") + "=" + "\"" + value + "\"" + " "
        return s
    
    def __repr__(self):
        return f'HTMLNode(\'{self.tag}\', \'{self.value}\', \'{self.children}\', \'{self.props}\')'
    
