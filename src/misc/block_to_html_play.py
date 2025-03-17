from service.utils.functions import (
    markdown_to_blocks,
    block_to_block
    )

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

