from django.utils import unittest
from wiki.templatetags.wikinotes_markup import wikinotes_markdown as md
	
class TestMarkdown(unittest.TestCase):

	elements = {
		"bold"						: "**bold**",
		"italic"					: "*italic*",
		"link"						: '[text](http://beta.wikinotes.ca "title")',
		"reflink"					: '[text]: http://beta.wikinotes.ca',
		"autolink"					: 'http://beta.wikinotes.ca',
		"image"						:'![alt](http://beta.wikinotes.ca/static/img/logo.png "title")',
		'inline'					: '`GetWindowHandleEx()`',
		'superscript'				: 'E=mc^2^',
		'subscript'					: 'CO~2~',
		'mention'					: '@dellsystem',
		'h1'						: '# header1 text',
		'h2'						: '## header2 text',
		'h3'						: '### header3 text',
		'h4'						: '#### header4 text',
		'h5'						: '##### header5 text',
		'alth1'						: 'header text\n-----------',
		'alth2'						: 'header text\n===========',
		'table'						:
									  "header 1 | header 2\n"
									  "---------|---------\n"
									  "content 1|content 2\n"
									  "content 3|content 4"
									  ,
		'table_alt'					:
									  "|header 1 | header 2|\n"
									  "|---------|---------|\n"
									  "|content 1|content 2|\n"
									  "|content 3|content 4|"
									  ,
		'table_align'				:
									"right | left |center\n"
									"-----:|:-----|:-----:\n"
									"c1    | c2   | c3\n"
									"c4    | c5   | c6\n"
									,
		'table_sort' 				:
									"header 1|header 2\n"
									"--------|------- sort\n"
									"c1		| c2\n"
									"c3		| c4\n"
									,
		'table_shampoo'				:
									"header 1|header 2\n"
									"--------|------- autumn\n"
									"c1		| c2\n"
									"c3		| c4\n"
									,
		'blockquote' 				:
									"> this is a quote\n"
									"> this is a second line\n"
									">\n"
									"> > nested quotes\n"
									">\n"
									"> back to the original\n"
									,
		'lists'						:
									"* item 1\n"
									"* item 2\n"
									"* item 3\n"
									,
		'num_list'					:
									"1. item 1\n"
									"2. item 2\n"
									"3. item 3\n"
									,
		'nested_lists'				:
									"* item 1\n"
									"* item 2\n"
									"	* sub 1 item 1\n"
									"	* sub 1 item 2\n"
									"		* sub 2 item 1\n"
									"	* sub 1 item 1\n"
									"* item 3\n"
									,
		'code_tabbed'				:
									"	public static void main(String [] args){\n"
									"		System.out.println('~*~*~*~');\n"
									"	}"
									,
		'code_fenced'				:
									"```\n"
									"def factorial(n):\n"
									"	return math.factorial(n)\n"
									"```",
		'code_highlight1'			:
									"```sml\n"
									"fun factorial 0 = 1 | factorial n = n * factorial(n-1)\n"
									"```",
		'code_highlight2'			:
									"	:::python\n"
									"	def hello():\n"
									"		print 'hello world!'"
									,
		'code_highlight3'			:
									"	#!/usr/bin/python\n"
									"	def goodbye():\n"
									"		print 'fuck this gay earth"
									,
		'line_num_tabbed'			:
									"	#!\n"
									"	so many\n"
									"	lines\n"
									"	here is one more line\n"
									,
		'line_num_fenced'			:
									"```!\n"
									"so many lines\n"
									"soooooo manyyyyyy linesssssssss\n"
									"```"
									,
		'line_num_fenced_lang'		:
									"```python\n"
									"def cake():\n"
									"	i_love_cake()\n"
									"```"
									,
		'line_num_tabbed_lang'		:
									"	#java!\n"
									"	public class GenericContainerInstanceManagerFactory{\n"
									"		public abstract String[] getInstanceRecord(){}\n"
									"	}",
		'horizontal_rules'			:
									"***",
		'definitions'				:
									"term\n"
									":	definition",
		'footnote'					:
									"This is a footnote[^1^]"
									"Even though it's on my head[^2^]"
									,
		'math'						:"$\sqrt{a^2+b^2}$",
		'merged_tables'				:
									"header 1 || header 2 merged\n"
									"---------|--------|--------\n"
									"c1       | c2     | c3\n"
									"||        entire row\n"
									"c5       || second two\n"
									"| first two | c6"
									}

	expected = {
		'line_num_fenced'			: 
									'<table class="codehilitetable"><tr><td class="linenos"><div class="linenodiv"><pre>1\n'
									'2</pre></div></td><td class="code"><div class="codehilite"><pre>so many lines\n'
									'soooooo manyyyyyy linesssssssss\n'
									'</pre></div>\n'
									'</td></tr></table>'
									,
		'autolink'					: '<p><a href="http://beta.wikinotes.ca">http://beta.wikinotes.ca</a></p>'
									,
		'blockquote'				: 
									'<blockquote>\n'
									'<p>this is a quote<br />\n'
									'this is a second line</p>\n'
									'<blockquote>\n'
									'<p>nested quotes</p>\n'
									'</blockquote>\n'
									'<p>back to the original</p>\n'
									'</blockquote>'
									,
		'lists'						: 
									'<ul>\n'
									'<li>item 1</li>\n'
									'<li>item 2</li>\n'
									'<li>item 3</li>\n'
									'</ul>'
									,
		'bold'						: '<p><strong>bold</strong></p>'
									,
		'code_tabbed'				: 
									'<div class="codehilite"><pre>public static void main(String [] args){\n'
									'    System.out.println(&#39;~*~*~*~&#39;);\n'
									'}\n'
									'</pre></div>'
									,
		'h2'						: '<h3 class="header" id="header2-text"><span>1</span>header2 text<a class="headerlink" href="#header2-text">&para;</a></h3>'
									,
		'h3'						: '<h4 class="header" id="header3-text"><span>1</span>header3 text<a class="headerlink" href="#header3-text">&para;</a></h4>'
									,
		'image'							: '<p><img alt="alt" src="http://beta.wikinotes.ca/static/img/logo.png" title="title" /></p>'
									,
		'h1'						: '<h2 class="header" id="header1-text"><span>1</span>header1 text<a class="headerlink" href="#header1-text">&para;</a></h2>'
									,
		'reflink'					: ''
									,
		'h4'						: '<h5 class="header" id="header4-text"><span>1</span>header4 text<a class="headerlink" href="#header4-text">&para;</a></h5>'
									,
		'h5'						: '<h6 class="header" id="header5-text"><span>1</span>header5 text<a class="headerlink" href="#header5-text">&para;</a></h6>'
									,
		'mention'					: '<p><a href="/user/dellsystem">@dellsystem</a></p>'
									,
		'horizontal_rules'			: '<hr />'
									,
		'link'						: '<p><a href="http://beta.wikinotes.ca" title="title">text</a></p>'
									,
		'table_sort'				: 
									'<table class="sort">\n'
									'<thead>\n'
									'<tr>\n'
									'<th>header 1</th>\n'
									'<th>header 2</th>\n'
									'</tr>\n'
									'</thead>\n'
									'<tbody>\n'
									'<tr>\n'
									'<td>c1</td>\n'
									'<td>c2</td>\n'
									'</tr>\n'
									'<tr>\n'
									'<td>c3</td>\n'
									'<td>c4</td>\n'
									'</tr>\n'
									'</tbody>\n'
									'</table>'
									,
		'line_num_fenced_lang'		: 
									'<div class="codehilite"><pre><span class="k">def</span> <span class="nf">cake</span><span class="p">():</span>\n'
									'    <span class="n">i_love_cake</span><span class="p">()</span>\n'
									'</pre></div>'
									,
		'table_alt'					: 
									'<table>\n'
									'<thead>\n'
									'<tr>\n'
									'<th>header 1</th>\n'
									'<th>header 2</th>\n'
									'</tr>\n'
									'</thead>\n'
									'<tbody>\n'
									'<tr>\n'
									'<td>content 1</td>\n'
									'<td>content 2</td>\n'
									'</tr>\n'
									'<tr>\n'
									'<td>content 3</td>\n'
									'<td>content 4</td>\n'
									'</tr>\n'
									'</tbody>\n'
									'</table>'
									,
		'table'						: 
									'<table>\n'
									'<thead>\n'
									'<tr>\n'
									'<th>header 1</th>\n'
									'<th>header 2</th>\n'
									'</tr>\n'
									'</thead>\n'
									'<tbody>\n'
									'<tr>\n'
									'<td>content 1</td>\n'
									'<td>content 2</td>\n'
									'</tr>\n'
									'<tr>\n'
									'<td>content 3</td>\n'
									'<td>content 4</td>\n'
									'</tr>\n'
									'</tbody>\n'
									'</table>'
									,
		'code_highlight2'			: 
									'<div class="codehilite"><pre><span class="k">def</span> <span class="nf">hello</span><span class="p">():</span>\n'
									'    <span class="k">print</span> <span class="s">&#39;hello world!&#39;</span>\n'
									'</pre></div>'
									,
		'nested_lists'				: 
									'<ul>\n'
									'<li>item 1</li>\n'
									'<li>item 2<ul>\n'
									'<li>sub 1 item 1</li>\n'
									'<li>sub 1 item 2<ul>\n'
									'<li>sub 2 item 1</li>\n'
									'</ul>\n'
									'</li>\n'
									'<li>sub 1 item 1</li>\n'
									'</ul>\n'
									'</li>\n'
									'<li>item 3</li>\n'
									'</ul>'
									,
		'code_highlight1'				: 
									'<div class="codehilite"><pre><span class="kr">'
									'fun</span> <span class="nf">factorial</span> <s'
									'pan class="mi">0</span> <span class="p">=</span>'
									' <span class="mi">1</span> <span class="p">|</spa'
									'n> <span class="nf">factorial</span> <span class="'
									'n">n</span> <span class="p">=</span> <span class="'
									'n">n</span> <span class="n">*</span> <span class="'
									'n">factorial</span><span class="p">(</span><span clas'
									's="n">n-</span><span class="mi">1</span><span cla'
									'ss="p">)</span>\n'
									'</pre></div>'
									,
		'alth1'				: '<h3 class="header" id="header-text"><span>1</span>header text<a class="headerlink" href="#header-text">&para;</a></h3>'
									,
		'alth2'				: '<h2 class="header" id="header-text"><span>1</span>header text<a class="headerlink" href="#header-text">&para;</a></h2>'
									,
		'table_align'				: 
									'<table>\n'
									'<thead>\n'
									'<tr>\n'
									'<th class="right-align">right</th>\n'
									'<th class="left-align">left</th>\n'
									'<th class="center-align">center</th>\n'
									'</tr>\n'
									'</thead>\n'
									'<tbody>\n'
									'<tr>\n'
									'<td class="right-align">c1</td>\n'
									'<td class="left-align">c2</td>\n'
									'<td class="center-align">c3</td>\n'
									'</tr>\n'
									'<tr>\n'
									'<td class="right-align">c4</td>\n'
									'<td class="left-align">c5</td>\n'
									'<td class="center-align">c6</td>\n'
									'</tr>\n'
									'</tbody>\n'
									'</table>'
									,
		'line_num_tabbed'				: 
									'<table class="codehilitetable"><tr><td class="linenos"><div class="linenodiv"><pre>1\n'
									'2\n'
									'3</pre></div></td><td class="code"><div class="codehilite"><pre>so many\n'
									'lines\n'
									'here is one more line\n'
									'</pre></div>\n'
									'</td></tr></table>'
									,
		'line_num_tabbed_lang'				: 
									'<table class="codehilitetable"><tr><td class="linenos"><div class="linenodiv"><pre>1\n'
									'2\n'
									'3\n'
									'4</pre></div></td><td class="code"><div class="codehilite"><pre>#java!\n'
									'public class GenericContainerInstanceManagerFactory{\n'
									'    public abstract String[] getInstanceRecord(){}\n'
									'}\n'
									'</pre></div>\n'
									'</td></tr></table>'
									,
		'footnote'					: "<p>This is a footnote[<sup>1</sup>]Even though it's on my head[<sup>2</sup>]</p>"
									,
		'table_shampoo'				: 
									'<table class="autumn">\n'
									'<thead>\n'
									'<tr>\n'
									'<th>header 1</th>\n'
									'<th>header 2</th>\n'
									'</tr>\n'
									'</thead>\n'
									'<tbody>\n'
									'<tr>\n'
									'<td>c1</td>\n'
									'<td>c2</td>\n'
									'</tr>\n'
									'<tr>\n'
									'<td>c3</td>\n'
									'<td>c4</td>\n'
									'</tr>\n'
									'</tbody>\n'
									'</table>'
									,
		'code_fenced'				: 
									'<div class="codehilite"><pre>def factorial(n):\n'
									'    return math.factorial(n)\n'
									'</pre></div>'
									,
		'definitions'				: 
									'<dl>\n'
									'<dt>term</dt>\n'
									'<dd>definition</dd>\n'
									'</dl>'
									,
		'code_highlight3'			: 
									'<table class="codehilitetable"><tr><td class="linenos"'
									'><div class="linenodiv"><pre>1\n2\n3</pre></div></td><'
									'td class="code"><div class="codehilite"><pre><span class'
									'="c">#!/usr/bin/python</span>\n<span class="k">def</span>'
									' <span class="nf">goodbye</span><span class="p">():</spa'
									'n>\n    <span class="k">print</span> <span class="s">&#39'
									';fuck this gay earth</span>\n</pre></div>\n</td></tr></table>'
									,
		'italic'					: '<p><em>italic</em></p>'
									,
		'inline'					: '<p><code>GetWindowHandleEx()</code></p>'
									,
		'subscript'					: '<p>CO<sub>2</sub></p>'
									,
		'num_list'					: 
									'<ol>\n'
									'<li>item 1</li>\n'
									'<li>item 2</li>\n'
									'<li>item 3</li>\n'
									'</ol>'
									,
		'math'						: '<p><span>$\sqrt{a^2+b^2}$</span></p>'
									,
		'superscript'				: '<p>E=mc<sup>2</sup></p>'
									,
		'merged_tables'				:
									"<table>\n"
									"<thead>\n"
									"<tr>\n"
									"<th>header 1</th>\n"
									"<th colspan=\"2\">header 2 merged</th>\n"
									"</tr>\n"
									"</thead>\n"
									"<tbody>\n"
									"<tr>\n"
									"<td>c1</td>\n"
									"<td>c2</td>\n"
									"<td>c3</td>\n"
									"</tr>\n"
									"<tr>\n"
									"<td colspan=\"3\">entire row</td>\n"
									"</tr>\n"
									"<tr>\n"
									"<td>c5</td>\n"
									"<td colspan=\"2\">second two</td>\n"
									"</tr>\n"
									"<tr>\n"
									"<td colspan=\"2\">first two</td>\n"
									"<td>c6</td>\n"
									"</tr>\n"
									"</tbody>\n"
									"</table>"
									
	}

	def generate_tests(cname, cparent, attr):
		def generate(key):
			def test(test):
				test.assertEqual(md(test.elements[key]),test.expected[key])
			return test

		for key in attr["elements"].keys():
			test_name = "test_"+key
			test_method = generate(key)
			attr[test_name] = test_method
		return type(cname, cparent, attr)
	
	__metaclass__ = generate_tests
