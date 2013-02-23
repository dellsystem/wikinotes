"""
To mention a user: @theirusername

Will add doctests later
"""

import markdown

# Global Vars
MENTION_RE = r'(?<![a-zA-Z0-9])@(?P<username>\w+)'
# '[@' + username + '](/user/' + username + ')'

class MentionPattern(markdown.inlinepatterns.Pattern):
    def handleMatch(self, m):
        username = m.group('username')

        el = markdown.util.etree.Element('a')
        el.text = '@' + username
        el.set('href', '/users/' + username)
        return el

class MentionExtension(markdown.Extension):

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns['mention'] = MentionPattern(MENTION_RE, md)

def makeExtension(configs=None):
    return MentionExtension(configs=configs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
