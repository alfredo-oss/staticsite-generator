text = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""

splits = text.split("\n\n")
splits = list(map(lambda x: x.strip(), splits))
print(splits)