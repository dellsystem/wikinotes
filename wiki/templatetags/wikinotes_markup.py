from django import template
from django.contrib.markup.templatetags.markup import markdown
from django.utils.html import escape

register = template.Library()

# NEEDS TESTS
@register.filter()
def wikinotes_markdown(value):
	return markdown(escape(value).replace('&amp;', '&').replace("\\$", "\\\\$"), 'tables,mathjax')

"""
The alternative to the escaping/removing-then-inserting ampersands thing (which must be done as both markdown and the escape function escape them) is to use just markdown with safe as one of the extensions, but that causes html to appear as [HTML_REMOVED] which is just silly. This way is much better.
"""
