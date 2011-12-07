from django import template
from django.utils.html import escape
import markdown

register = template.Library()

md = markdown.Markdown(extensions=['subscript', 'superscript', 'urlize', 'nl2br', 'def_list', 'tables', 'mathjax', 'toc', 'footnotes'], safe_mode='escape', output_format='xhtml1')

# NEEDS TESTS
@register.filter()
def wikinotes_markdown(value):
	# Replace \$ with \\$ so that markdown doesn't do anything else to (in conjunction with mathjax's processEscapes)
	return md.convert(value.replace("\\$", "\\\\$"))
