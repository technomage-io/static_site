from enum import Enum, auto
import re




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

def split_nodes_image(old_nodes):
    new_nodes = []

    image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

    for node in old_nodes:
        # Only split TEXT nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = list(re.finditer(image_pattern, text))

        if not matches:
            new_nodes.append(node)
            continue

        last_index = 0

        for match in matches:
            start, end = match.span()
            alt_text, url = match.groups()

            # Add text before the image
            if start > last_index:
                new_nodes.append(
                    TextNode(text[last_index:start], TextType.TEXT)
                )

            # Add the image node
            new_nodes.append(
                TextNode(alt_text, TextType.IMAGE, url)
            )

            last_index = end

        # Add remaining text after last match
        if last_index < len(text):
            new_nodes.append(
                TextNode(text[last_index:], TextType.TEXT)
            )

    return new_nodes




def split_nodes_link(old_nodes):
    new_nodes = []

    link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"


    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = list(re.finditer(link_pattern, text))

        if not matches:
            new_nodes.append(node)
            continue

        last_index = 0

        for match in matches:
            start, end = match.span()
            anchor_text, url = match.groups()

            # Add text before the link
            if start > last_index:
                new_nodes.append(
                    TextNode(text[last_index:start], TextType.TEXT)
                )

            # Add the link node
            new_nodes.append(
                TextNode(anchor_text, TextType.LINK, url)
            )

            last_index = end

        # Add remaining text after last match
        if last_index < len(text):
            new_nodes.append(
                TextNode(text[last_index:], TextType.TEXT)
            )

    return new_nodes






def text_to_textnodes(text):
    # Start with one raw text node
    nodes = [TextNode(text, TextType.TEXT)]

    # Extract images first
    nodes = split_nodes_image(nodes)

    # Extract links next
    nodes = split_nodes_link(nodes)

    # Then apply formatting delimiters
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    return nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches



def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

