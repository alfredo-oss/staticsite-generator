import unittest
from service.nodes.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_prop_to_str(self):
        props = {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        prop_rep = HTMLNode("a", "embrace the random", None, **props).props_to_html()
        res = " href=\"https://www.google.com\" target=\"_blank\" "    
        self.assertEqual(prop_rep, res)

    def test_repr(self):
        props = {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        string_rep = repr(HTMLNode("a", "embrace the random", None, **props))
        res = f"HTMLNode(\'a\', \'embrace the random\', \'None\', \'{props}\')"
        self.assertEqual(string_rep, res)
    
if __name__ == "__main__":
    unittest.main()

