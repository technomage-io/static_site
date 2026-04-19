import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import (
    TextNode,
    TextType,
    BlockType,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
    text_to_textnodes,
)
from markdown import (
    markdown_to_blocks,
    markdown_to_html_node,
    block_to_block_type,
)
from converter import text_node_to_html_node




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

def test_split_nodes_image_single(self):
    node = TextNode(
        "Here is an image ![alt](http://img.com/a.png) in text",
        TextType.TEXT
    )
    result = split_nodes_image([node])

    expected = [
        TextNode("Here is an image ", TextType.TEXT),
        TextNode("alt", TextType.IMAGE, "http://img.com/a.png"),
        TextNode(" in text", TextType.TEXT),
    ]

    self.assertListEqual(result, expected)

def test_split_nodes_image_multiple(self):
    node = TextNode(
        "Start ![one](url1) middle ![two](url2) end",
        TextType.TEXT
    )
    result = split_nodes_image([node])

    expected = [
         TextNode("Start ", TextType.TEXT),
         TextNode("one", TextType.IMAGE, "url1"),
         TextNode(" middle ", TextType.TEXT),
         TextNode("two", TextType.IMAGE, "url2"),
         TextNode(" end", TextType.TEXT),
    ]

    self.assertListEqual(result, expected) 

def test_split_nodes_image_none(self):
    node = TextNode(
        "There are no images here.",
        TextType.TEXT
    )
    result = split_nodes_image([node])

    expected = [node]  # unchanged

    self.assertListEqual(result, expected)

def test_split_nodes_image_none(self):
    node = TextNode(
        "There are no images here.",
        TextType.TEXT
    )
    result = split_nodes_image([node])

    expected = [node]  # unchanged

    self.assertListEqual(result, expected)

def test_split_nodes_link_multiple(self):
    node = TextNode(
        "Go to [one](url1) or maybe [two](url2)",
        TextType.TEXT
    )
    result = split_nodes_link([node])

    expected = [
        TextNode("Go to ", TextType.TEXT),
        TextNode("one", TextType.LINK, "url1"),
        TextNode(" or maybe ", TextType.TEXT),
        TextNode("two", TextType.LINK, "url2"),
    ]

    self.assertListEqual(result, expected)

def test_split_nodes_link_none(self):
    node = TextNode(
        "There are no links here.",
        TextType.TEXT
    )
    result = split_nodes_link([node])

    expected = [node]  # unchanged

    self.assertListEqual(result, expected)    

def test_text_to_textnodes_mixed_formatting(self):
    text = "Here is **bold**, _italic_, and `code`."
    result = text_to_textnodes(text)

    expected = [
        TextNode("Here is ", TextType.TEXT),
        TextNode("bold", TextType.BOLD),
        TextNode(", ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(", and ", TextType.TEXT),
        TextNode("code", TextType.CODE),
        TextNode(".", TextType.TEXT),
    ]

    self.assertEqual(result, expected)

def test_text_to_textnodes_image_and_link(self):
    text = "Pic: ![cat](cat.png) and a [link](https://boot.dev)"
    result = text_to_textnodes(text)

    expected = [
        TextNode("Pic: ", TextType.TEXT),
        TextNode("cat", TextType.IMAGE, "cat.png"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
    ]

    self.assertEqual(result, expected)

def test_text_to_textnodes_full_example(self):
    text = (
        "This is **text** with an _italic_ word and a `code block` "
        "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
        "and a [link](https://boot.dev)"
    )

    result = text_to_textnodes(text)

    expected = [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
    ]

    self.assertEqual(result, expected)

def test_basic_blocks():
    md = """# This is a heading

This is a paragraph.

- item 1
- item 2
"""
    expected = [
        "# This is a heading",
        "This is a paragraph.",
        "- item 1\n- item 2"
    ]
    assert markdown_to_blocks(md) == expected
            
def test_extra_blank_lines():
    md = """# Title



Paragraph text.



"""
    expected = [
        "# Title",
        "Paragraph text."
    ]
    assert markdown_to_blocks(md) == expected

def test_strip_whitespace():
    md = """   # Heading    

    Paragraph with spaces.    

"""
    expected = [
        "# Heading",
        "Paragraph with spaces."
    ]
    assert markdown_to_blocks(md) == expected


def test_single_block():
    md = "# Only one block here"
    expected = ["# Only one block here"]
    assert markdown_to_blocks(md) == expected

def test_multiple_lists():
    md = """- a
- b

- c
- d
"""
    expected = [
        "- a\n- b",
        "- c\n- d"
    ]
    assert markdown_to_blocks(md) == expected

def test_heading_levels(self):
    self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
    self.assertEqual(block_to_block_type("###### Six levels"), BlockType.HEADING)

def test_invalid_heading_missing_space(self):
    self.assertEqual(block_to_block_type("#Heading"), BlockType.PARAGRAPH)

def test_code_block(self):
   md = "```\nprint('hello')\n```"
   self.assertEqual(block_to_block_type(md), BlockType.CODE)

def test_code_block_empty(self):
    md = "```\n```"
    self.assertEqual(block_to_block_type(md), BlockType.CODE)

def test_quote_block(self):
    md = "> quote line 1\n> quote line 2"
    self.assertEqual(block_to_block_type(md), BlockType.QUOTE)

def test_quote_block_with_optional_space(self):
    md = "> quote\n>    more quote"
    self.assertEqual(block_to_block_type(md), BlockType.QUOTE)

def test_invalid_quote_block(self):
    md = "> valid\nnot valid"
    self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

def test_unordered_list(self):
    md = "- item 1\n- item 2\n- item 3"
    self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)

def test_invalid_unordered_list_missing_space(self):
    md = "-item 1\n- item 2"
    self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

def test_ordered_list(self):
    md = "1. first\n2. second\n3. third"
    self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)

def test_ordered_list_wrong_start_number(self):
    md = "2. wrong\n3. wrong"
    self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

def test_ordered_list_wrong_increment(self):
    md = "1. ok\n3. wrong"
    self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

def test_paragraph_default(self):
    md = "This is just a normal paragraph of text."
    self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

def test_single_heading(self):
        md = "# Hello World"
        root = markdown_to_html_node(md)

        self.assertEqual(root.tag, "div")
        self.assertEqual(len(root.children), 1)

        h1 = root.children[0]
        self.assertEqual(h1.tag, "h1")
        self.assertEqual(h1.children[0].text, "Hello World")

def test_paragraph(self):
        md = "This is a paragraph."
        root = markdown_to_html_node(md)

        self.assertEqual(len(root.children), 1)
        p = root.children[0]
        self.assertEqual(p.tag, "p")
        self.assertEqual(p.children[0].text, "This is a paragraph.")

def test_unordered_list(self):
        md = "- a\n- b\n- c"
        root = markdown_to_html_node(md)

        ul = root.children[0]
        self.assertEqual(ul.tag, "ul")
        self.assertEqual(len(ul.children), 3)

        self.assertEqual(ul.children[0].tag, "li")
        self.assertEqual(ul.children[0].children[0].text, "a")

def test_ordered_list(self):
        md = "1. first\n2. second\n3. third"
        root = markdown_to_html_node(md)

        ol = root.children[0]
        self.assertEqual(ol.tag, "ol")
        self.assertEqual(len(ol.children), 3)

        self.assertEqual(ol.children[1].children[0].text, "second")

def test_quote_block(self):
        md = "> hello\n> world"
        root = markdown_to_html_node(md)

        blockquote = root.children[0]
        self.assertEqual(blockquote.tag, "blockquote")

        # Inline parser usually merges into one text node
        text = blockquote.children[0].text
        self.assertIn("hello", text)
        self.assertIn("world", text)

def test_code_block(self):
        md = "```\nprint('hi')\n```"
        root = markdown_to_html_node(md)

        pre = root.children[0]
        self.assertEqual(pre.tag, "pre")

        code = pre.children[0]
        self.assertEqual(code.tag, "code")

        text_node = code.children[0]
        self.assertEqual(text_node.text, "print('hi')")

def test_multiple_blocks(self):
        md = """# Title

Paragraph text.

- a
- b
"""
        root = markdown_to_html_node(md)

        self.assertEqual(len(root.children), 3)

        self.assertEqual(root.children[0].tag, "h1")
        self.assertEqual(root.children[1].tag, "p")
        self.assertEqual(root.children[2].tag, "ul")






if __name__ == "__main__":
    unittest.main()