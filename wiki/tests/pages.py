from django.test import TestCase

from wiki.utils.pages import get_section_start_end


class TestSectionEdit(TestCase):
    lines = [
        '# lol',                    # 0
        '## lol',                   # 1
        '# lol',                    # 2
        '# text',                   # 3
        'blah blah blah',           # 4
        '## Some subsection',       # 5
        'blah blah',                # 6
        '### Another subsection',   # 7
        '# Going back up',          # 8
        'text',                     # 9
        '```',                      # 10
        '# text',                   # 11
        '```',                      # 12
        '# Text',                   # 13
    ]
    tests = {
        # The first section
        'lol': (0, 2),
        # The first subsection'
        'lol_1': (1, 2),
        # A non-existent section
        'header': (0, 14),
        # Another section
        'lol_2': (2, 3),
        # Another non-existent section
        'lol_3': (0, 14),
        # A longer section
        'text': (3, 8),
        # Another subsection
        'some-subsection': (5, 8),
        # Deeper subsection
        'another-subsection': (7, 8),
        # Another section
        'going-back-up': (8, 13),
        # Ignoring code blocks
        'text_1': (13, 14),
    }

    def runTest(self):
        for anchor, expected in self.tests.iteritems():
            actual = get_section_start_end(self.lines, anchor)
            self.assertEqual(actual, expected)
