import textwrap

from ..preprocess import Metadata

import unittest


class MetadataTest(unittest.TestCase):

    def test_extract_cell_metadata_basic(self):
        metadata = Metadata.extract_cell_metadata(textwrap.dedent("""\
            # Animal Farm
            + Author: George Orwell
            + Date: 1945-08-17
        """))
        expected = {
            'title': 'Animal Farm',
            'author': 'George Orwell',
            'date': '1945-08-17',
        }
        self.assertEqual(expected, metadata)

    def test_extract_cell_metadata_other_bullets(self):
        metadata = Metadata.extract_cell_metadata(textwrap.dedent("""\
            # Animal Farm
            - Author: George Orwell
            * Date: 1945-08-17
            Tags: books
        """))
        expected = {
            'title': 'Animal Farm',
            'author': 'George Orwell',
            'date': '1945-08-17',
            'tags': 'books',
        }
        self.assertEqual(expected, metadata)

    def test_extract_cell_metadata_title_variation(self):
        metadata = Metadata.extract_cell_metadata(textwrap.dedent("""\
            + Author: George Orwell
            ## Animal Farm
            + Date: 1945-08-17
        """))
        expected = {
            'title': 'Animal Farm',
            'author': 'George Orwell',
            'date': '1945-08-17',
        }
        self.assertEqual(expected, metadata)

    def test_extract_cell_metadata_whitespace(self):
        metadata = Metadata.extract_cell_metadata(textwrap.dedent("""\
            #  Animal Farm
               +  Author   :   George Orwell
               +  Date     :   1945-08-17
        """))
        expected = {
            'title': 'Animal Farm',
            'author': 'George Orwell',
            'date': '1945-08-17',
        }
        self.assertEqual(expected, metadata)
