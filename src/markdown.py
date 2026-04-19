from htmlnode import ParentNode, LeafNode, HTMLNode
from textnode import TextNode, BlockType
from converter import text_to_children, text_node_to_html_node




def block_to_block_type(block):
    lines = block.split("\n")

    # 1. Heading: 1–6 # characters, then a space
    if lines[0].startswith("#"):
        i = 0
        while i < len(lines[0]) and lines[0][i] == "#":
            i += 1
        if 1 <= i <= 6 and i < len(lines[0]) and lines[0][i] == " ":
            return BlockType.HEADING

    # 2. Code block: starts with ``` + newline, ends with ```
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    # 3. Quote block: every line starts with >
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # 4. Unordered list: every line starts with "- "
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # 5. Ordered list: lines must be "1. ", "2. ", "3. ", ...
    ordered = True
    for i, line in enumerate(lines, start=1):
        prefix = f"{i}. "
        if not line.startswith(prefix):
            ordered = False
            break
    if ordered:
        return BlockType.ORDERED_LIST

    # 6. Otherwise: paragraph
    return BlockType.PARAGRAPH





def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    # Start with a simple container that can be empty
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            node = heading_to_html_node(block)
        elif block_type == BlockType.PARAGRAPH:
            node = paragraph_to_html_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            node = unordered_list_to_html_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            node = ordered_list_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            node = quote_to_html_node(block)
        elif block_type == BlockType.CODE:
            node = code_block_to_html_node(block)
        else:
            raise ValueError(f"Unknown block type: {block_type}")

        children.append(node)

    # NOW we can safely create a ParentNode
    return ParentNode("div", children)


def markdown_to_blocks(markdown):
    # Split on double newlines to get raw blocks
    raw_blocks = markdown.split("\n\n")

    blocks = []
    for block in raw_blocks:
        cleaned = block.strip()
        if cleaned:          # ignore empty blocks
            blocks.append(cleaned)

    return blocks


def heading_to_html_node(block):
    # Count leading #'s
    i = 0
    while i < len(block) and block[i] == "#":
        i += 1

    level = i
    text = block[level+1:]  # skip "#... "

    children = text_to_children(text)
    return ParentNode(f"h{level}", children=children)

def paragraph_to_html_node(block):
    children = text_to_children(block)
    return ParentNode("p", children=children)

def unordered_list_to_html_node(block):
    lines = block.split("\n")
    items = []

    for line in lines:
        text = line[2:]  # remove "- "
        li_children = text_to_children(text)
        items.append(ParentNode("li", children=li_children))

    return ParentNode("ul", children=items)

def ordered_list_to_html_node(block):
    lines = block.split("\n")
    items = []

    for line in lines:
        # remove "1. ", "2. ", etc.
        dot_index = line.index(".")
        text = line[dot_index + 2:]
        li_children = text_to_children(text)
        items.append(ParentNode("li", children=li_children))

    return ParentNode("ol", children=items)

def quote_to_html_node(block):
    lines = block.split("\n")
    stripped = [line[1:].lstrip() for line in lines]  # remove ">"

    # Join back into a single paragraph inside <blockquote>
    text = " ".join(stripped)
    children = text_to_children(text)

    return ParentNode("blockquote", children=children)


def code_block_to_html_node(block):
    # Remove the ``` wrapper
    inner = block[4:-3]

    # Code blocks should NOT be inline parsed
    code_child = LeafNode(None, inner)
    code_node = ParentNode("code", [code_child])
    return ParentNode("pre", [code_node])

def extract_title(markdown: str) -> str:
    """
    Extract the first H1 title from the markdown string.
    An H1 is a line that starts with a single '#' followed by a space or text.
    Raises a ValueError if no H1 is found.
    """
    lines = markdown.split("\n")

    for line in lines:
        stripped = line.strip()
        # Must start with exactly one '#' followed by a space or text
        if stripped.startswith("#"):
            # Count leading '#'
            i = 0
            while i < len(stripped) and stripped[i] == "#":
                i += 1

            # Only accept a single '#'
            if i == 1:
                # Get the rest of the line after '#'
                title = stripped[i:].strip()
                if title:
                    return title

    raise Exception("No H1 title found in markdown")