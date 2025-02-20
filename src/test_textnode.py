import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a banana", TextType.ITALIC)
        node2 = TextNode("This is an apple", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_plus_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.alfred.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.alfred.com")
        self.assertEqual(node, node2)

    def test_neq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()