"""Plot.ly extension for Markdown.

Expected format: {plot dellsystem 0}
"""

import markdown

PLOTLY_RE = r'\{plot ([^ ]+) (\d+)\}'
WIDTH = 940
HEIGHT = 500

class PlotLyPattern(markdown.inlinepatterns.Pattern):
    def handleMatch(self, m):
        username = m.group(2)
        plot_id = m.group(3)

        el = markdown.util.etree.Element('iframe')
        el.attrib['width'] = str(WIDTH)
        el.attrib['height'] = str(HEIGHT)
        el.attrib['scrolling'] = 'no'
        el.attrib['seamless'] = 'seamless'
        el.attrib['src'] = 'https://plot.ly/~%s/%s/%d/%d' % (username,
                                                             plot_id,
                                                             WIDTH,
                                                             HEIGHT)
        return el

class PlotLyExtension(markdown.Extension):
    """Plot.ly extension for Python-Markdown. """

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns['plotly'] = PlotLyPattern(PLOTLY_RE, md)

def makeExtension(configs=None):
    return PlotLyExtension(configs=configs)
