import markdown

# Global Vars
MENTION_RE = r'(?<![a-zA-Z0-9_])@\w+'

class MentionPattern(markdown.inlinepatterns.Pattern):
	def handleMatch(self, m):
		text = m.group(0)
		username = text[1:]
		path = '/user/' + username

		el = markdown.util.etree.Element("a")
		el.text = markdown.util.AtomicString(text)
		el.set('href', path)
		el.set('title', 'User: ' + username)
		return el

class MentionExtension(markdown.Extension):
	def extendMarkdown(self, md, md_globals):
		""" Replace subscript with SubscriptPattern """
		md.inlinePatterns['mentions'] = MentionPattern(MENTION_RE, md)

def makeExtension(configs=None):
	return MentionExtension(configs=configs)
