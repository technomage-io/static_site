from textnode import TextNode, TextType
from copystatic import copy_directory


def main():
    node = TextNode(
        "This is some anchor text",
        TextType.LINK,
        "https://www.boot.dev"
    )
    print(node)

def main():
    copy_directory("static", "public")
    print("Static files copied successfully.")


if __name__ == "__main__":
    main()

