from leafnode import LeafNode
import unittest

class TestLeafNode(unittest.TestCase):
    def test_leaf_representation(self):
        props = {
                "href": "https://www.google.com"
            }
        node = LeafNode("a", "juju", **props).to_html()
        res = "<a href=\"https://www.google.com\" >juju</a>"
        self.assertEqual(node, res)

if __name__ == "__main__":
    unittest.main()