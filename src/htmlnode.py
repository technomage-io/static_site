import re

from textnode import TextNode, TextType

from textnode import split_nodes_delimiter


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError("to_html() must be implemented by subclasses")
    
    def props_to_html(self):
        if not self.props:
            return ""
        props_str = " ".join(f'{key}="{value}"' for key, value in self.props.items())
        return f" {props_str}"
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        
        if value is None:
            raise ValueError("LeafNode must have a value")
          
        super().__init__(tag=tag, value=value, children=[], props=props)

    def to_html(self):
        
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        
        if self.tag is None:
            return self.value
        
             
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"  
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError("ParentNode must have a tag")  
       
        if children is None or len(children) == 0:
            raise ValueError("ParentNode must have children")   

        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag to convert to HTML")
        
        if not self.children:
            raise ValueError("ParentNode must have children to convert to HTML")


        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"
    


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches



def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

import re

from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError("to_html() must be implemented by subclasses")
    
    def props_to_html(self):
        if not self.props:
            return ""
        props_str = " ".join(f'{key}="{value}"' for key, value in self.props.items())
        return f" {props_str}"
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        
        if value is None:
            raise ValueError("LeafNode must have a value")
          
        super().__init__(tag=tag, value=value, children=[], props=props)

    def to_html(self):
        
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        
        if self.tag is None:
            return self.value
        
             
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"  
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError("ParentNode must have a tag")  
       
        if children is None or len(children) == 0:
            raise ValueError("ParentNode must have children")   

        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag to convert to HTML")
        
        if not self.children:
            raise ValueError("ParentNode must have children to convert to HTML")


        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"
    


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches



def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

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






def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        # Only operate on TEXT nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)

        # No links → return original node
        if not links:
            new_nodes.append(node)
            continue

        # Process links one by one
        for anchor, url in links:
            markdown = f"[{anchor}]({url})"
            before, after = text.split(markdown, 1)

            # Add text before link (if not empty)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            # Add link node
            new_nodes.append(TextNode(anchor, TextType.LINK, url))

            # Continue processing the remainder
            text = after

        # Add leftover text (if not empty)
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

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

def markdown_to_blocks(markdown):
    # Split on double newlines to get raw blocks
    raw_blocks = markdown.split("\n\n")

    blocks = []
    for block in raw_blocks:
        cleaned = block.strip()
        if cleaned:          # ignore empty blocks
            blocks.append(cleaned)

    return blocks