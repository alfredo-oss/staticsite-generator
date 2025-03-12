from service.nodes.textnode import TextNode, TextType
import unittest
from service.utils.functions import split_nodes_delimiter

class TestMDtoTextNode(unittest.TestCase):
    ######### tests `` code block transformation #########
    def test_raw_code_to_text_single(self):
        raw_md = [TextNode("This is text with a `code block` word", TextType.NORMAL)]
        delimiter = "`"
        text_type = TextType.CODE
        expected = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
        ]
        res = split_nodes_delimiter(raw_md, delimiter, text_type)
        self.assertEqual(res, expected)

    def test_raw_code_to_text_multiple(self):
        raw_md = [TextNode("This is text with a `code block` word", TextType.NORMAL), TextNode("This is text with a `code block` word", TextType.NORMAL)]
        delimiter = "`"
        text_type = TextType.CODE
        expected = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL)
        ]
        res = split_nodes_delimiter(raw_md, delimiter, text_type)
        self.assertEqual(res, expected)

    ######### tests ** bold ** code bold transformation #########
    def test_raw_code_to_text_single(self):
        raw_md = [TextNode("This is text with a **bold block** word", TextType.NORMAL)]
        delimiter = "**"
        text_type = TextType.CODE
        expected = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.NORMAL),
        ]
        res = split_nodes_delimiter(raw_md, delimiter, text_type)
        self.assertEqual(res, expected)
    
    def test_raw_code_to_text_multiple(self):
        raw_md = [TextNode("This is text with a **bold block** word", TextType.NORMAL), TextNode("This is text with a **bold block** word", TextType.NORMAL)]
        delimiter = "**"
        text_type = TextType.CODE
        expected = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.NORMAL),
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.NORMAL)
        ]
        res = split_nodes_delimiter(raw_md, delimiter, text_type)
        self.assertEqual(res, expected)

    ######### tests _ italic _ code italic transformation #########
    def test_raw_code_to_text_single(self):
        raw_md = [TextNode("This is text with an _italic block_ word", TextType.NORMAL)]
        delimiter = "_"
        text_type = TextType.ITALIC
        expected = [
            TextNode("This is text with an ", TextType.NORMAL),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.NORMAL),
        ]
        res = split_nodes_delimiter(raw_md, delimiter, text_type)
        self.assertEqual(res, expected)

    def test_raw_code_to_text_multiple(self):
        raw_md = [TextNode("This is text with an _italic block_ word", TextType.NORMAL), TextNode("This is text with an _italic block_ word", TextType.NORMAL)]
        delimiter = "_"
        text_type = TextType.ITALIC
        expected = [
            TextNode("This is text with an ", TextType.NORMAL),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.NORMAL),
            TextNode("This is text with an ", TextType.NORMAL),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.NORMAL)
        ]
        res = split_nodes_delimiter(raw_md, delimiter, text_type)
        self.assertEqual(res, expected)