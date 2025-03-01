from service.nodes.leafnode import LeafNode
import unittest

class TestLeafNode(unittest.TestCase):
    def test_leaf_representation(self):
        props = {
                "href": "https://www.google.com"
            }
        node = LeafNode("a", "juju", **props).to_html()
        res = "<a href=\"https://www.google.com\" >juju</a>"
        self.assertEqual(node, res)
    
    def test_no_value(self):
        props = {
                "href": "https://www.google.com"
            }
        with self.assertRaises(ValueError):
            LeafNode(tag="a", value=None, **props).to_html()

    def test_no_tag(self):
        props = {
                "href": "https://www.google.com"
            }
        node = LeafNode(tag=None, value="juju", **props)

if __name__ == "__main__":
    unittest.main()