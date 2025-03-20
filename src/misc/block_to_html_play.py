from service.utils.functions import (
    markdown_to_blocks,
    block_to_block
    )
from service.blocks.block_types import BlockType
from service.nodes.parentnode import ParentNode

## once this is separated, we have to keep in mind that it needs to be joined again
md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

expected_result = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"

md_blocks = markdown_to_blocks(md)

for block in md_blocks:
    print(f"BLOCK {block} is of type: {block_to_block(block)}")
    match block_to_block(block):
        case BlockType.paragraph:
            print(ParentNode('p', block).to_html())
        case BlockType.heading:
            print(ParentNode('h1', block).to_html())
        case BlockType.code:
            print(ParentNode('code', block).to_html())
        case BlockType.quote:
            print(ParentNode('blockquote', block).to_html())
        case BlockType.unordered_list:
            print(ParentNode('ul', block).to_html())
        case BlockType.ordered_list:
            print(ParentNode('ol', block).to_html())
