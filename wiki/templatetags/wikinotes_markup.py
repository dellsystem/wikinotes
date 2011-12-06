from django import template
from django.contrib.markup.templatetags.markup import markdown
from django.utils.html import escape

register = template.Library()

# NEEDS TESTS
@register.filter()
def wikinotes_markdown(value):
	return markdown(escape(value).replace('&amp;', '&').replace("\\$", "\\\\$"), 'mathjax')
