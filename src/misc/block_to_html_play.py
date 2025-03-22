from service.utils.functions import (
    text_to_textnodes,
    markdown_to_blocks,
    text_node_to_html_node,
    block_to_block
    )
from service.blocks.block_types import BlockType
from service.nodes.parentnode import ParentNode
from service.nodes.leafnode import LeafNode

## once this is separated, we have to keep in mind that it needs to be joined again
md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
md2 = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

expected_result = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"

md_blocks = markdown_to_blocks(md)

### testing block transformation from text to HTML 
# raw text

multiple_text_nodes = list(map(lambda x: text_to_textnodes(x.replace('\n', ' ')), md_blocks))
#print(multiple_text_nodes)
## transform to normal TextNode
#block_text_nodes = text_to_textnodes(block)
html_nodes = list(map(lambda x: list(map(lambda y: text_node_to_html_node(y), x)), multiple_text_nodes))
#print(html_nodes[0])
#html_nodes = list(map(lambda x: (text_node_to_html_node(x)).to_html(), block_text_nodes))

res = []
for block in md_blocks:
    match block_to_block(block):
        case BlockType.paragraph:
            res.append(ParentNode('p', list(map(lambda y: text_node_to_html_node(y), text_to_textnodes(block.replace('\n', ' ')))))) #.replace('\n', ' ')
        case BlockType.heading:
            res.append(ParentNode('h1', list(map(lambda y: text_node_to_html_node(y), text_to_textnodes(block.replace('\n', ' '))))))
        case BlockType.code:
            res.append(ParentNode('pre',[LeafNode('code', block.replace("```", ""))]))
        case BlockType.quote:
            res.append(ParentNode('blockquote', list(map(lambda y: text_node_to_html_node(y), text_to_textnodes(block.replace('\n', ' '))))))
        case BlockType.unordered_list:
            res.append(ParentNode('ul', list(map(lambda y: text_node_to_html_node(y), text_to_textnodes(block.replace('\n', ' '))))))
        case BlockType.ordered_list:
            res.append(ParentNode('ol', list(map(lambda y: text_node_to_html_node(y), text_to_textnodes(block).replace('\n', ' ')))))
print(ParentNode('div',res).to_html())
