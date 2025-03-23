from service.utils.functions import block_to_block
from service.blocks.block_types import BlockType
import unittest

class TestBlockToBlock(unittest.TestCase):
    def test_heading_block(self):
        block = "## This is a heading"
        block_type = block_to_block(block)
        self.assertEqual(block_type, BlockType.heading)

    def test_code_block(self):
        block = "```import pandas as pd```"
        block_type = block_to_block(block)
        self.assertEqual(block_type, BlockType.code)

    def test_quote_block(self):
        block = "> This is a quote"
        block_type = block_to_block(block)
        self.assertEqual(block_type, BlockType.quote)

    def test_unordered_list_block(self):
        block = "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        block_type = block_to_block(block)
        self.assertEqual(block_type, BlockType.unordered_list)

    def test_ordered_list_block(self):
        block = "1. This is the first list item in a list block\n2. This is a list item\n3. This is another list item"
        block_type = block_to_block(block)
        self.assertEqual(block_type, BlockType.ordered_list)

    def test_paragraph_block(self):
        block = "This is a normal paragraph"
        block_type = block_to_block(block)
        self.assertEqual(block_type, BlockType.paragraph)