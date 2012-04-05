from django import template
from django.utils.html import escape
import markdown
import re

register = template.Library()

"""
Extensions are either part of the standard markdown library or located in the root directory, as mdx_{extension name}.py

Standard extensions used, unmodified:
	* footnotes
	* nl2br

All extensions beginning with wiki_ are modified version of standard extensions.
"""

md = markdown.Markdown(extensions=['wiki_footnotes', 'wiki_toc', 'downheader', 'wiki_tables', 'wiki_codehilite', 'wiki_fenced_code', 'wiki_def_list', 'nl2br', 'subscript', 'superscript', 'mathjax', 'urlize', 'wikilinks'], safe_mode='escape', output_format='xhtml1')

# NEEDS TESTS
@register.filter()
def wikinotes_markdown(value):
	# Must reset it to clear the footnotes and maybe other stuff too
	md.reset()
	# Replace \$ with \\$ so that markdown doesn't do anything else to (in conjunction with mathjax's processEscapes)
	return md.convert(value)
