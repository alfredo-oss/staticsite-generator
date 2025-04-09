import re
from service.nodes.textnode import TextNode, TextType
from service.utils.functions import (
markdown_to_html_node
)
from collections import deque

italic_string = """
As we stand at the threshold of this mystical realm, it is clear that _The Lord of the Rings_ is not merely a series but a gateway to a world that continues to enchant and inspire. It is a beacon of imagination, a wellspring of wisdom, and a testament to the power of myth. In the grand tapestry of fantasy literature, Tolkien's masterpiece is the gleaming jewel in the crown, unmatched in its majesty and enduring in its legacy. As an Archmage who has traversed the myriad realms of magic and lore, I declare with utmost conviction: _The Lord of the Rings_ reigns supreme as the greatest legendarium our world has ever known.
"""

bold_string = """In J.R.R. Tolkien's legendarium, characterized by its rich tapestry of noble heroes and epic deeds, two Elven luminaries stand out: **Glorfindel**, the stalwart warrior returned from the Halls of Mandos, and **Legolas**, the prince of the Woodland Realm. While both possess grace and valor beyond mortal ken, it is Glorfindel who emerges as the more compelling figure, a beacon of heroism whose legacy spans ages."""

code_string = """An elaborate pantheon of deities (the `Valar` and `Maiar`)"""

def parse_multi_nested_nodes(objective_string: str):
    italic_matches = re.findall(r"_(.*?)_", objective_string) 
    bold_matches = re.findall(r"\*\*(.*?)\*\*", objective_string)
    code_matches = re.findall(r"`(.*?)`", objective_string)
    splits = []
    multi_match = [(italic_matches, TextType.ITALIC, "_"), (bold_matches, TextType.BOLD, "**"), (code_matches, TextType.CODE, "`")]
    for matches, match_type, split_string in multi_match:
        if split_string in objective_string:
            matches = deque(matches)
            splits = objective_string.split(split_string)
            i = 0
            while matches:
                matching_string = matches.popleft() 
                while i < len(splits):
                    if splits[i] == matching_string:
                        splits[i] = TextNode(matching_string, match_type)
                        i += 1
                    i += 1
        else: 
            continue
    return splits

print(parse_multi_nested_nodes(italic_string))
print(parse_multi_nested_nodes(bold_string))
print(parse_multi_nested_nodes(code_string))


