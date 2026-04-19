import unittest
from markdown import extract_title  

class TestExtractTitle(unittest.TestCase):

    def test_simple_title(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_title_with_spaces(self):
        markdown = "   #   My Title   "
        self.assertEqual(extract_title(markdown), "My Title")

    def test_title_not_first_line(self):
        markdown = "Some intro text\n# Real Title\nMore text"
        self.assertEqual(extract_title(markdown), "Real Title")

    def test_multiple_headings(self):
        markdown = "# First Title\n## Subtitle\n# Another Title"
        self.assertEqual(extract_title(markdown), "First Title")

    def test_no_h1_raises(self):
        markdown = "## Not an H1\n### Also not\nJust text"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_h2_should_not_be_accepted(self):
        markdown = "## Wrong Level"
        with self.assertRaises(Exception):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()
