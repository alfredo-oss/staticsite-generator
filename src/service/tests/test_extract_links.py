from service.nodes.textnode import TextNode, TextType
from service.utils.functions import split_nodes_link
import unittest

class TestImageRegexExtraction(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an [link](https://alfred.com/vlog) and another [second link](https://alfred.com/contact)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("link", TextType.IMAGE, "https://alfred.com/vlog"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second link", TextType.IMAGE, "https://alfred.com/contact"
                ),
            ],
            new_nodes,
        )