from platform import node
import unittest
from converter import text_node_to_html_node
from htmlnode import HTMLNode, ParentNode
from htmlnode import LeafNode
from textnode import TextNode, TextType, split_nodes_delimiter
from htmlnode import extract_markdown_images, extract_markdown_links


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

    def test_text_to_html_text(self):
        node = TextNode("hello", TextType.TEXT)
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), "hello")

    def test_text_to_html_bold(self):
        node = TextNode("bold", TextType.BOLD)
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), "<b>bold</b>")

    def test_text_to_html_italic(self):
        node = TextNode("italics", TextType.ITALIC)
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), "<i>italics</i>")

    def test_text_to_html_code(self):
        node = TextNode("print()", TextType.CODE)
        html = text_node_to_html_node(node)
        self.assertEqual(html.to_html(), "<code>print()</code>")

    def test_text_to_html_link(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        html = text_node_to_html_node(node)
        self.assertEqual(
            html.to_html(),
            '<a href="https://boot.dev">Boot.dev</a>'
    )

    def test_text_to_html_image(self):
        node = TextNode("A cat", TextType.IMAGE, "cat.png")
        html = text_node_to_html_node(node)
        self.assertEqual(
            html.to_html(),
            '<img src="cat.png" alt="A cat"></img>'
    ) 

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_inline_code(self):
        node = TextNode("Hello `world`!", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(result, [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.CODE),
            TextNode("!", TextType.TEXT),
        ])

    def test_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ])

    def test_italic(self):
        node = TextNode("Some _italic_ words", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(result, [
            TextNode("Some ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" words", TextType.TEXT),
        ])

    def test_multiple_code_spans(self):
        node = TextNode("A `one` B `two` C", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(result, [
            TextNode("A ", TextType.TEXT),
            TextNode("one", TextType.CODE),
            TextNode(" B ", TextType.TEXT),
            TextNode("two", TextType.CODE),
            TextNode(" C", TextType.TEXT),
        ])

    def test_no_delimiter_present(self):
        node = TextNode("Just plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(result, [
            TextNode("Just plain text", TextType.TEXT)
        ])

    def test_unbalanced_delimiter(self):
        node = TextNode("This is `broken text", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_non_text_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(result, [node])

def test_multiple_images(self):
    text = "![one](url1) and ![two](url2)"
    matches = extract_markdown_images(text)
    self.assertListEqual(
        [("one", "url1"), ("two", "url2")],
        matches
    )

def test_extract_markdown_links(self):
    matches = extract_markdown_links(
        "Here is a [link](https://example.com)"
    )
    self.assertListEqual(
        [("link", "https://example.com")],
        matches
    )   
def test_links_ignore_images(self):
    text = "![img](url1) and [real link](url2)"
    matches = extract_markdown_links(text)
    self.assertListEqual(
        [("real link", "url2")],
        matches
    )
if __name__ == "__main__":
    unittest.main()