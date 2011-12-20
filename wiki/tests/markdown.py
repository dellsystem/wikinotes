from django.test import TestCase
from wiki.templatetags.wikinotes_markup import wikinotes_markdown

# Use the formatting guide as a comprehensive test case, because it has pretty much everything
class TestFormattingGuide(TestCase):
	expected = """<p>Wikinotes uses a superset of the <strong><a href="http://daringfireball.net/projects/markdown/syntax">Markdown</a></strong> markup language for formatting wiki pages. If you've never used it before, you may wish to give this guide a read and keep it as a reference when editing pages. If you're already familiar with Markdown, note that there are a few differences between the Markdown we use here and standard markdown. The new features we incorporate are the following:</p>
<ul>
<li><a href="#tables">Tables</a></li>
<li><a href="#footnotes">Footnotes</a></li>
<li><a href="#definition-lists">Definition lists</a></li>
<li><a href="#subscript-and-superscript">Subscript and superscript</a></li>
<li><a href="#math-markup-with-mathjax">Math markup with MathJax</a></li>
<li><a href="#code-blocks">Syntax highlighting and fenced code blocks</a></li>
</ul>
<p>We've also modified the following aspects of standard Markdown behaviour:</p>
<ul>
<li><a href="#line-breaks">Line breaks from new lines</a></li>
<li><a href="#inline-html">Inline HTML</a></li>
<li><a href="#automatic-linking">Automatic linking</a></li>
<li><a href="#italics">Underscores in the middle of a word</a></li>
</ul>
<p>We've tried to keep the formatting style as simple, concise and readable as possible, while still allowing for a wide range of formatting options. Elements have been borrowed from <a href="http://github.github.com/github-flavored-markdown/">GitHub Flavored Markdown (GFM)</a> and <a href="http://stackoverflow.com/editing-help">StackOverflow's Markdown</a>, and some of the additional features were inspired by what was available on our MediaWiki site. Below you can find a fairly comprehensive listing of the components of Wikinotes Markdown, but if there's something you're not sure about, don't hestitate to <a href="/about#contact-us">shoot us an email</a>.</p>
<p>You can find the source of our Markdown parser (which uses the python-markdown library and several extensions) in our <a href="https://github.com/dellsystem/wikinotes/blob/master/wiki/templatetags/wikinotes_markup.py">GitHub repository</a>. The markdown source for this page can be found <a href="later">within the repository</a> as well.</p>
<div class="toc">
<ul>
<li><a href="#inline-elements">1 Inline elements</a><ul>
<li><a href="#emphasis">1.1 Emphasis</a><ul>
<li><a href="#bold">1.1.1 Bold</a></li>
<li><a href="#italics">1.1.2 Italics</a></li>
<li><a href="#underline">1.1.3 Underline</a></li>
</ul>
</li>
<li><a href="#links">1.2 Links</a><ul>
<li><a href="#standard-links">1.2.1 Standard links</a></li>
<li><a href="#reference-style-links">1.2.2 Reference-style links</a></li>
<li><a href="#automatic-linking">1.2.3 Automatic linking</a></li>
</ul>
</li>
<li><a href="#images">1.3 Images</a><ul>
<li><a href="#image-syntax">1.3.1 Image syntax</a></li>
<li><a href="#policy-on-outside-images">1.3.2 Policy on outside images</a></li>
</ul>
</li>
<li><a href="#inline-code">1.4 Inline code</a></li>
<li><a href="#subscript-and-superscript">1.5 Subscript and superscript</a></li>
</ul>
</li>
<li><a href="#block-elements">2 Block elements</a><ul>
<li><a href="#headers">2.1 Headers</a><ul>
<li><a href="#header-syntax">2.1.1 Header syntax</a></li>
<li><a href="#alternative-syntax">2.1.2 Alternative syntax</a></li>
<li><a href="#section-numbers">2.1.3 Section numbers</a></li>
<li><a href="#mapping-to-html-headers">2.1.4 Mapping to HTML headers</a></li>
</ul>
</li>
<li><a href="#paragraphs">2.2 Paragraphs</a></li>
<li><a href="#tables">2.3 Tables</a><ul>
<li><a href="#creating-a-table">2.3.1 Creating a table</a></li>
<li><a href="#column-alignment">2.3.2 Column alignment</a></li>
<li><a href="#allowing-sorting">2.3.3 Allowing sorting</a></li>
<li><a href="#changing-the-colour-scheme">2.3.4 Changing the colour scheme</a></li>
</ul>
</li>
<li><a href="#blockquotes">2.4 Blockquotes</a></li>
<li><a href="#lists">2.5 Lists</a></li>
<li><a href="#code-blocks">2.6 Code blocks</a><ul>
<li><a href="#tabbed-code-blocks">2.6.1 Tabbed code blocks</a></li>
<li><a href="#fenced-code-blocks">2.6.2 Fenced code blocks</a></li>
<li><a href="#syntax-highlighting">2.6.3 Syntax highlighting</a></li>
<li><a href="#line-numbers">2.6.4 Line numbers</a></li>
</ul>
</li>
<li><a href="#horizontal-rules">2.7 Horizontal rules</a></li>
<li><a href="#definition-lists">2.8 Definition lists</a></li>
<li><a href="#footnotes">2.9 Footnotes</a></li>
</ul>
</li>
<li><a href="#miscellaneous">3 Miscellaneous</a><ul>
<li><a href="#line-breaks">3.1 Line breaks</a></li>
<li><a href="#inline-html">3.2 Inline HTML</a></li>
<li><a href="#math-markup">3.3 Math markup</a></li>
<li><a href="#escaping-things">3.4 Escaping things</a></li>
</ul>
</li>
</ul>
</div>
<h2 id="inline-elements"><span>1</span>Inline elements</h2>
<h3 id="emphasis"><span>1.1</span>Emphasis</h3>
<h4 id="bold"><span>1.1.1</span>Bold</h4>
<p>To make a section of text <strong>bold</strong>, simply put two asterisks or two underscore characters around it, as in the following:</p>
<div class="codehilite"><pre>**this will be bold**
__this will also be bold__
</pre></div>


<p>If you want to enter two asterisks or two underscore characters <em>without</em> bolding anything, you can escape them. For example, <code>\*\*</code> will produce **, and <code>\_\_</code> will produce __.</p>
<h4 id="italics"><span>1.1.2</span>Italics</h4>
<p>To <em>italicise</em> a section of text, simply put one asterisk or one underscore character on each side of it, as in the following:</p>
<div class="codehilite"><pre>*this will be italicised*
_this will be italicised_
</pre></div>


<p>As before, entering one underscore or one asterisk can be done by escaping it with the backslash character. <code>\*</code> becomes * and <code>\_</code> becomes _. Alternatively, surround them with spaces: <code>*</code> or <code>_</code>.</p>
<p>Underscores in the middle of a word (e.g. some_variable or this_should_work) will not be treated as emphasis. This differs from standard markdown, but is the default behaviour of the python-markdown library as well as GFM.</p>
<h4 id="underline"><span>1.1.3</span>Underline</h4>
<p>Markdown does not support underlining, mainly because that could cause underlined words to be confused with hyperlinks, and we don't plan on adding it.</p>
<h3 id="links"><span>1.2</span>Links</h3>
<h4 id="standard-links"><span>1.2.1</span>Standard links</h4>
<p>Use <code>[text to display](http://www.example.com)</code> to link to something. Relative links work as well; for example, <a href="#standard-links">this</a> is an anchor link to this section and <a href="/help/formatting">this</a> is a link to this page, relative to the base of this site. You can also add a title attribute (i.e. the text that appears when you hover over a link) by enclosing it within double quotes at the end of the link: <code>[text to display](http://www.example.com "This is title text")</code>.</p>
<p>Make sure to include the <code>http://</code> (or whatever protocol it is) when linking to something off-site.</p>
<h4 id="reference-style-links"><span>1.2.2</span>Reference-style links</h4>
<p>Standard Markdown has support for reference-style links, e.g. <code>[text to display][some link]</code> where <code>[some link]</code> is defined later on in the document, like this:</p>
<div class="codehilite"><pre><span class="p">[</span><span class="n">some</span> <span class="n">link</span><span class="p">]:</span> <span class="n">http</span><span class="p">:</span><span class="o">//</span><span class="n">www</span><span class="o">.</span><span class="n">example</span><span class="o">.</span><span class="n">com</span>
</pre></div>


<p>We don't encourage the use of this style except in cases where it really offers an improvement. You can learn more about this <a href="http://daringfireball.net/projects/markdown/syntax#link">here</a>.</p>
<h4 id="automatic-linking"><span>1.2.3</span>Automatic linking</h4>
<p>If you just enter <a href="http://www.example.com">http://www.example.com</a> it will automatically link it. Same with <a href="http://www.example.com">www.example.com</a>, <a href="http://www.wikinotes.ca/help">www.wikinotes.ca/help</a>, and other such obvious links. If a URL isn't automatically linked, you can of course use the standard link feature mentioned above. The <a href="https://github.com/r0wb0t/markdown-urlize">urlize</a> Markdown extension is used for this.</p>
<h3 id="images"><span>1.3</span>Images</h3>
<h4 id="image-syntax"><span>1.3.1</span>Image syntax</h4>
<p>The syntax is similar to the link syntax, except with a ! at the front:</p>
<div class="codehilite"><pre>![Alt text](http://beta.wikinotes.ca/static/img/logo.png &quot;Title text&quot;)
</pre></div>


<p>will produce</p>
<p><img alt="Alt text" src="http://beta.wikinotes.ca/static/img/logo.png" title="Title text" /></p>
<p>The alt text must be specified, although it can be left empty if so desired. The title text is optional.</p>
<h4 id="policy-on-outside-images"><span>1.3.2</span>Policy on outside images</h4>
<p>If you find an image that you want to incorporate into a page, please first make sure that you have permission to use it, and check for license compatibility. (You can find out more about copyright issues on Wikinotes <a href="/help/copyright">here</a>.) We don't recommend hotlinking - we will eventually have an image uploading feature, but until that has been created we suggest reuploading the image somewhere such as <a href="http://www.imgur.com">www.imgur.com</a> or your <a href="http://cs.mcgill.ca">cs.mcgill.ca</a> website if you have one.</p>
<h3 id="inline-code"><span>1.4</span>Inline code</h3>
<p>The syntax is the same as in <a href="http://daringfireball.net/projects/markdown/syntax#code">standard Markdown</a> - just use backticks (`) to enclose inline code. For example, <code>some_function_name()</code>.  To enter a backtick by itself, escape it: `. To enter a single backtick within inline code, you can use multiple backticks as the delimiters.</p>
<h3 id="subscript-and-superscript"><span>1.5</span>Subscript and superscript</h3>
<p>Subscript is just <sub>this</sub>. Superscript is <sup>this</sup>. Syntax:</p>
<div class="codehilite"><pre>CO~2~ for subscript
E=mc^2^ for superscript
</pre></div>


<p>We use the <a href="https://github.com/sgraber/markdown.subscript">subscript</a> and <a href="https://github.com/sgraber/markdown.superscript">superscript</a> extensions written by Shane Graber for this.</p>
<p>If you need to write mathematical expressions, it is preferred that you use <a href="#math-markup">LaTeX math markup</a>, which will be processed by MathJax and converted into beautifully typeset math.</p>
<h2 id="block-elements"><span>2</span>Block elements</h2>
<h3 id="headers"><span>2.1</span>Headers</h3>
<h4 id="header-syntax"><span>2.1.1</span>Header syntax</h4>
<p>Like <code># Header text</code> or <code>## Header text</code>, all the way up to five <code>#</code>'s. The space is not necessary (<code>#Header text</code> would work, for example) and you can place the same number of <code>#</code>'s on the other side as well, but for cleanness as consistency, we recommend the syntax above. We also prefer that only the first word be capitalised.</p>
<h4 id="alternative-syntax"><span>2.1.2</span>Alternative syntax</h4>
<p>The following Setext-style syntax for top-level and second-level headers would work as well:</p>
<div class="codehilite"><pre><span class="n">Test</span>
<span class="o">----</span>
<span class="n">Test</span>
<span class="o">====</span>
</pre></div>


<p>However, we prefer the <a href="#header-syntax">aforementioned</a> Atx-style headers because they have a wider range and necessitate fewer characters.</p>
<h4 id="section-numbers"><span>2.1.3</span>Section numbers</h4>
<p>Automatic section numbering is automatic. You can't disable it. Sorry.</p>
<h4 id="mapping-to-html-headers"><span>2.1.4</span>Mapping to HTML headers</h4>
<p>Typically, a <code># Header</code> will become <code>&lt;h1&gt;Header&lt;/h1&gt;</code>, <code>## Header</code> will become <code>&lt;h2&gt;Header&lt;/h2&gt;</code>, and so on. However, we use the <a href="http://code.google.com/p/markdown-downheader/">downheader</a> Markdown extension to convert <code># Header</code> into <code>&lt;h2&gt;Header&lt;/h2&gt;</code>, etc (with the smallest header being <code>##### Header</code>, an <code>&lt;h6&gt;</code> element). This is because having more than one h1 element on a page doesn't make much sense, semantically.</p>
<h3 id="paragraphs"><span>2.2</span>Paragraphs</h3>
<p>Surround a block of text with empty lines (or just nothing) before and after it and bam, paragraph.</p>
<h3 id="tables"><span>2.3</span>Tables</h3>
<h4 id="creating-a-table"><span>2.3.1</span>Creating a table</h4>
<p>A basic example:</p>
<div class="codehilite"><pre>Header cell 1 | Header cell 2
------------- | -------------
Content cell 1 | Content cell 2
Content cell 3 | Content cell 4
</pre></div>


<p>becomes</p>
<table>
<thead>
<tr>
<th>Header cell 1</th>
<th>Header cell 2</th>
</tr>
</thead>
<tbody>
<tr>
<td>Content cell 1</td>
<td>Content cell 2</td>
</tr>
<tr>
<td>Content cell 3</td>
<td>Content cell 4</td>
</tr>
</tbody>
</table>
<p>The pipe (|) characters don't have to be lined up. It's also possible to put the pipes on the outside as well, although this is not necessary:</p>
<div class="codehilite"><pre>|Header cell 1 | Header cell 2|
|------------- | -------------|
|Content cell 1 | Content cell 2|
|Content cell 3 | Content cell 4|
</pre></div>


<h4 id="column-alignment"><span>2.3.2</span>Column alignment</h4>
<p>You can align individual columns using a colon (:) to indicate the direction of alignment. For example:</p>
<table>
<thead>
<tr>
<th class="right-align">Right alignment</th>
<th class="left-align">Left alignment</th>
<th class="center-align">Center alignment</th>
</tr>
</thead>
<tbody>
<tr>
<td class="right-align">Content cell 1</td>
<td class="left-align">Content cell 2</td>
<td class="center-align">Content cell 3</td>
</tr>
<tr>
<td class="right-align">Content cell 4</td>
<td class="left-align">Content cell 4</td>
<td class="center-align">Content cell 6</td>
</tr>
</tbody>
</table>
<h4 id="allowing-sorting"><span>2.3.3</span>Allowing sorting</h4>
<p>By default, tables can not be sorted. If you want a table to be sortable via the <a href="http://tablesorter.com/docs/">jQuery tablesorter plugin</a>, add the "sort" class to it, like this:</p>
<div class="codehilite"><pre>Header cell 1 | Header cell 2
------------- | ------------- sort
Content cell 1 | Content cell 2
Content cell 3 | Content cell 4
</pre></div>


<p>which will result in a table whose rows are sortable by the cell values per column, by clicking on the column headers:</p>
<table class="sort">
<thead>
<tr>
<th>Header cell 1</th>
<th>Header cell 2</th>
</tr>
</thead>
<tbody>
<tr>
<td>Content cell 1</td>
<td>Content cell 2</td>
</tr>
<tr>
<td>Content cell 3</td>
<td>Content cell 4</td>
</tr>
</tbody>
</table>
<h4 id="changing-the-colour-scheme"><span>2.3.4</span>Changing the colour scheme</h4>
<p>Besides the "sort" class, the following classes can be placed at the end of the second line in a table, separated by a space:</p>
<ul>
<li>clear</li>
<li>autumn</li>
<li>lights</li>
<li>fresh</li>
<li>ribbon</li>
<li>iris</li>
</ul>
<p>These all indicate colour schemes for the tables. The <code>autumn</code> colour scheme looks as follows:</p>
<table class="autumn">
<thead>
<tr>
<th>Header cell 1</th>
<th>Header cell 2</th>
</tr>
</thead>
<tbody>
<tr>
<td>Content cell 1</td>
<td>Content cell 2</td>
</tr>
<tr>
<td>Content cell 3</td>
<td>Content cell 4</td>
</tr>
</tbody>
</table>
<p>You can specify multiple colour schemes (or add the <code>sort</code> attribute) for one table by separating them with spaces, although it might not turn out the way you want. Still, feel free to experiment.</p>
<h3 id="blockquotes"><span>2.4</span>Blockquotes</h3>
<p>Same as in <a href="http://daringfireball.net/projects/markdown/syntax#blockquote">regular markdown</a>. You can nest them, and add other block elements as well.</p>
<h3 id="lists"><span>2.5</span>Lists</h3>
<p>Same as in <a href="http://daringfireball.net/projects/markdown/syntax#list">regular markdown</a>.</p>
<h3 id="code-blocks"><span>2.6</span>Code blocks</h3>
<h4 id="tabbed-code-blocks"><span>2.6.1</span>Tabbed code blocks</h4>
<p>As in <a href="http://daringfireball.net/projects/markdown/syntax#precode">standard Markdown</a>, you can create a code block by indenting each line with four spaces or a tab. Relative indentation is preserved, and you shouldn't need to escape anything (HTML- and Markdown-specific special characters are converted automatically, for example).</p>
<h4 id="fenced-code-blocks"><span>2.6.2</span>Fenced code blocks</h4>
<p>You can also create fenced code blocks, which allow you to insert code as above but without having to manually indent anything. Just wrap the block with 3 backtick characters or 3 tilde characters. For example:</p>
<div class="codehilite"><pre>```
def some_function(some_param):
    some_var = some_param &gt; 0
    do_something(some_var)
```
</pre></div>


<p>We use the <a href="http://freewisdom.org/projects/python-markdown/Fenced_Code_Blocks">fenced code blocks</a> extension found in the standard Markdown library, with some modifications to make it more similar to GFM.</p>
<h4 id="syntax-highlighting"><span>2.6.3</span>Syntax highlighting</h4>
<p>We use Pygments and a modified version of the <a href="http://freewisdom.org/projects/python-markdown/CodeHilite">CodeHilite</a> extension to provide syntax highlighting for tabbed or fenced code. You can set the language in several ways depending on whether you use tabbing or fencing for your code block. For example:</p>
<div class="codehilite"><pre>```python
def some_function(some_param):
    some_var = some_param &gt; 0
    do_something(some_var)
```
</pre></div>


<p>and</p>
<div class="codehilite"><pre>    :::python
    def some_function(some_param):
        some_var = some_param &gt; 0
        do_something(some_var)
</pre></div>


<p>will direct Pygments to use Python as the highlighting language, which will appear as follows:</p>
<div class="codehilite"><pre><span class="k">def</span> <span class="nf">some_function</span><span class="p">(</span><span class="n">some_param</span><span class="p">):</span>
    <span class="n">some_var</span> <span class="o">=</span> <span class="n">some_param</span> <span class="o">&gt;</span> <span class="mi">0</span>
    <span class="n">do_something</span><span class="p">(</span><span class="n">some_var</span><span class="p">)</span>
</pre></div>


<p>You can also set the language by including a <a href="http://en.wikipedia.org/wiki/Shebang_(Unix)">shebang</a> line at the beginning of the code block:</p>
<div class="codehilite"><pre>    #!/usr/bin/python
    def some_function(some_param):
        some_var = some_param &gt; 0
        do_something(some_var)
</pre></div>


<p>will result in </p>
<table class="codehilitetable"><tr><td class="linenos"><div class="linenodiv"><pre>1
2
3
4</pre></div></td><td class="code"><div class="codehilite"><pre><span class="c">#!/usr/bin/python</span>
<span class="k">def</span> <span class="nf">some_function</span><span class="p">(</span><span class="n">some_param</span><span class="p">):</span>
    <span class="n">some_var</span> <span class="o">=</span> <span class="n">some_param</span> <span class="o">&gt;</span> <span class="mi">0</span>
    <span class="n">do_something</span><span class="p">(</span><span class="n">some_var</span><span class="p">)</span>
</pre></div>
</td></tr></table>

<p>Including a shebang line will always trigger the appearance of line numbers, although you can get around them by setting the language in another way; see the section on <a href="#line-numbers">line numbers</a> below for more.</p>
<p>If you don't set the language, Pygments will not try to guess the language, and so the code will appear in one colour.</p>
<h4 id="line-numbers"><span>2.6.4</span>Line numbers</h4>
<p>If you're going to be discussing a code block on a page, we recommend the use of line numbers. There are four different ways to force line numbers, depending on whether or not you set the language and whether you use tabbing or fencing.</p>
<p>Tabbed, no language set:</p>
<div class="codehilite"><pre>    #!
    this is a code block
    spanning multiple lines
</pre></div>


<p>Fenced, no language set:</p>
<div class="codehilite"><pre>```!
this is a code block
spanning multiple lines
```
</pre></div>


<p>Both of the above will result in:</p>
<table class="codehilitetable"><tr><td class="linenos"><div class="linenodiv"><pre>1
2</pre></div></td><td class="code"><div class="codehilite"><pre>this is a code block
spanning multiple lines
</pre></div>
</td></tr></table>

<p>Tabbed, language set:</p>
<div class="codehilite"><pre>    #python!
    def some_function(some_param):
        some_var = some_param &gt; 0
        do_something(some_var)
</pre></div>


<p>Fenced, language set:</p>
<div class="codehilite"><pre>```python!
def some_function(some_param):
    some_var = some_param &gt; 0
    do_something(some_var)
```
</pre></div>


<p>Both of the above will result in:</p>
<table class="codehilitetable"><tr><td class="linenos"><div class="linenodiv"><pre>1
2
3</pre></div></td><td class="code"><div class="codehilite"><pre><span class="k">def</span> <span class="nf">some_function</span><span class="p">(</span><span class="n">some_param</span><span class="p">):</span>
    <span class="n">some_var</span> <span class="o">=</span> <span class="n">some_param</span> <span class="o">&gt;</span> <span class="mi">0</span>
    <span class="n">do_something</span><span class="p">(</span><span class="n">some_var</span><span class="p">)</span>
</pre></div>
</td></tr></table>

<p>If you want to disable line numbers on a code block that includes the shebang line, simply use <code>:::</code> as the first line. You'll have to set the language separately if you want it to be highlighted, though.</p>
<h3 id="horizontal-rules"><span>2.7</span>Horizontal rules</h3>
<p>You can create a horizontal rule using three or more asterisks, like this:</p>
<div class="codehilite"><pre>***
</pre></div>


<p>which will produce</p>
<hr />
<p>See the <a href="http://daringfireball.net/projects/markdown/syntax#hr">standard Markdown documentation on this</a> for more.</p>
<h3 id="definition-lists"><span>2.8</span>Definition lists</h3>
<p>We use a slightly modified version of the <a href="http://freewisdom.org/projects/python-markdown/Definition_Lists">definition list</a> extension included with the standard Markdown library. A definition list is contained within a &lt;dl&gt;&lt;/dl&gt; element, with each term within a &lt;dt&gt;&lt;/dt&gt; and each definition within a &lt;dd&gt;&lt;/dd&gt;. An example should suffice:</p>
<div class="codehilite"><pre>term
: definition
: another def
term
another term
: a def
last term
: definition
</pre></div>


<p>turns into</p>
<dl>
<dt>term</dt>
<dd>definition</dd>
<dd>another def</dd>
<dt>term</dt>
<dt>another term</dt>
<dd>a def</dd>
<dt>last term</dt>
<dd>definition</dd>
</dl>
<p>Useful for vocabulary lists and the like.</p>
<h3 id="footnotes"><span>2.9</span>Footnotes</h3>
<p>We use the <a href="http://freewisdom.org/projects/python-markdown/Footnotes">footnotes</a> extension included in the standard Markdown library to add footnote functionality, similar to that which is available with MediaWiki. Footnotes can be defined using the following syntax:</p>
<div class="codehilite"><pre>This is text[^1^] and more text[^2^]
</pre></div>


<p>will become: This is text<sup id="fnref:1"><a href="#fn:1" rel="footnote">1</a></sup> and more text<sup id="fnref:2"><a href="#fn:2" rel="footnote">2</a></sup></p>
<p>Although the footnotes will automatically become numbers, you don't need to number them properly, or even use numbers:</p>
<div class="codehilite"><pre>This is text[^lol] and more text[^5]
</pre></div>


<p>will show up as: This is text<sup id="fnref:lol"><a href="#fn:lol" rel="footnote">3</a></sup> and more text<sup id="fnref:5"><a href="#fn:5" rel="footnote">4</a></sup>.</p>
<p>You can define footnotes at the bottom of the page. (Or rather, anything after the footnotes will be considered part of the footnotes.) Footnote definitions can be multiple lines, with blockquotes, code blocks, and other block elements. Just be sure to indent subsequent lines with an additional four spaces (or tab).</p>
<p>Although failing to define a footnote won't break anything, it may mess up the formatting a bit, so we don't recommend it.</p>
<h2 id="miscellaneous"><span>3</span>Miscellaneous</h2>
<h3 id="line-breaks"><span>3.1</span>Line breaks</h3>
<p>Same as StackOverflow and GFM. A new line becomes a line break. For example:</p>
<div class="codehilite"><pre>This is a haiku
Or at least it will be soon
After this line ends
</pre></div>


<p>This is a haiku<br />
Or at least it will be soon<br />
After this line ends</p>
<p>Included as an extension in the standard Markdown library as of version 2.1.0.</p>
<h3 id="inline-html"><span>3.2</span>Inline HTML</h3>
<p>HTML tags are automatically escaped for security reasons.<sup id="fnref:lolwebct"><a href="#fn:lolwebct" rel="footnote">5</a></sup> If there's some styling or formatting technique you need that doesn't have an adequate Markdown replacement, please <a href="/about#contact-us">let us know</a>.</p>
<h3 id="math-markup"><span>3.3</span>Math markup</h3>
<p>We use <a href="http://www.mathjax.org/">MathJax</a> for client-side processing of LaTeX math markup. There is a fairly useful list on <a href="">Wikipedia</a> of the most common symbols and expressions. Instead of &lt;math&gt;&lt;/math&gt; tags, we use the dollar sign - \$ for inline, \$\$ for display. For example:</p>
<div class="codehilite"><pre>This is text $a^2 + b^2 = c^2$ and that was the Pythagorean theorem.
</pre></div>


<p>will turn into</p>
<p>This is text <span>$a^2 + b^2 = c^2$</span> and that was the Pythagorean theorem.</p>
<p>For display math, which will be horizontally centered on the page, use two \$'s. For example:</p>
<div class="codehilite"><pre>This is text

$$\sqrt{a^2 + b^2 = c^2}$$

That was centered
</pre></div>


<p>will be rendered as</p>
<p>This is text</p>
<p><span>$$\sqrt{a^2 + b^2 = c^2}$$</span></p>
<p>That was centered</p>
<p>You can also force display-style math within inline math. For example, <code>$\int_x^{\infty}$</code> displays as <span>$\int_x^{\infty}$</span>, but if you add <code>\displaystyle</code> to the beginning of the expression, it appears instead as <span>$\displaystyle \int_x^{\infty}$</span></p>
<p>To insert a \$ without meaning for it to delimit math, escape it, like this: <code>\\$</code></p>
<h3 id="escaping-things"><span>3.4</span>Escaping things</h3>
<p>Most special characters can be escaped with a backslash. You can find more information in the <a href="http://daringfireball.net/projects/markdown/syntax#backslash">Markdown documentation</a>.</p>
<div class="footnote">
<hr />
<ol>
<li id="fn:1">
<p>lol&#160;<a href="#fnref:1" rev="footnote" title="Jump back to footnote 1 in the text">&#8617;</a></p>
</li>
<li id="fn:2">
<p>lol&#160;<a href="#fnref:2" rev="footnote" title="Jump back to footnote 2 in the text">&#8617;</a></p>
</li>
<li id="fn:lol">
<p>lol&#160;<a href="#fnref:lol" rev="footnote" title="Jump back to footnote 3 in the text">&#8617;</a></p>
</li>
<li id="fn:5">
<p>lol&#160;<a href="#fnref:5" rev="footnote" title="Jump back to footnote 4 in the text">&#8617;</a></p>
</li>
<li id="fn:lolwebct">
<p>lol&#160;<a href="#fnref:lolwebct" rev="footnote" title="Jump back to footnote 5 in the text">&#8617;</a></p>
</li>
</ol>
</div>"""
	def setUp(self):
		self.raw = open('templates/help/formatting.md').read()

	def test_markdown(self):
		self.assertEqual(wikinotes_markdown(self.raw), self.expected)
