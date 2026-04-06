import unittest
from htmlnode import HTMLNode, ParentNode
from htmlnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children, [])
      
        self.assertEqual(
            node.props, {})
       

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        
        self.assertEqual(
            repr(node),
            "HTMLNode(tag=p, value=What a strange world, children=[], props={'class': 'primary'})"
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")

        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_raw_text(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click", {"href": "https://google.com"})
        self.assertEqual(
        node.to_html(),
        '<a href="https://google.com">Click</a>'
    )

    def test_leaf_missing_value_raises(self):
        with self.assertRaises(ValueError):
         LeafNode("p", None)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
    )
        
    def test_parentnode_missing_tag_raises(self):
        child = LeafNode("p", "text")
        with self.assertRaises(ValueError):
             ParentNode(None, [child])


    def test_parentnode_missing_children_raises(self):
       with self.assertRaises(ValueError):
            ParentNode("div", None)


    def test_parentnode_empty_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", [])


def test_parentnode_mixed_children(self):
    child1 = LeafNode("b", "Bold")
    child2 = ParentNode("span", [LeafNode(None, "inner")])
    parent = ParentNode("div", [child1, child2])

    self.assertEqual(
        parent.to_html(),
        "<div><b>Bold</b><span>inner</span></div>",
    )

     


if __name__ == "__main__":
    unittest.main()