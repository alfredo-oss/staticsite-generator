from service.nodes.textnode import TextNode, TextType
import unittest
from service.utils.functions import split_nodes_delimiter

class TestMDtoTextNode(unittest.TestCase):
    def test_raw_to_text(self):
        raw_md = [TextNode("This is text with a `code block` word", TextType.NORMAL)]
        delimiter = "`"
        text_type = TextType.CODE
        expected = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
        ]
        res = split_nodes_delimiter(raw_md, delimiter, text_type)
        print(res, expected)
        # i think this is generating an error
        self.assertEqual(res[1], expected[1])