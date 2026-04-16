from enum import Enum, auto

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
   
class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue


        parts = node.text.split(delimiter)
        
        if len(parts) % 2 == 0:
            raise Exception(f"Invalid Markdown: Unmatched delimiter {delimiter}")
        for i, part in enumerate(parts):    
            if part == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type)) 
                        
    return new_nodes

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