import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_assertEqual(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_assertNotEqual(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
        
    def test_equal_with_default_url(self):
        node = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Hello", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal_url(self):
        node = TextNode("Hello", TextType.BOLD, url=None)
        node2 = TextNode("Hello", TextType.BOLD, url="https://example.com")
        self.assertNotEqual(node, node2)

    def test_all_properties_different(self):
        node = TextNode("Hello", TextType.BOLD, url=None)
        node2 = TextNode("Goodbye", TextType.ITALIC, url="https://example.com")
        self.assertNotEqual(node, node2)


    
if __name__ == "__main__":
    unittest.main()