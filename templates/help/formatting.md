Wikinotes uses a superset of the **[Markdown](http://daringfireball.net/projects/markdown/syntax)** markup language for formatting wiki pages. If you've never used it before, you may wish to give this guide a read and keep it as a reference when editing pages. If you're already familiar with Markdown, note that there are a few differences between the Markdown we use here and standard markdown. The new features we incorporate are the following:

* [Tables](#tables)
* [Footnotes](#footnotes)
* [Definition lists](#definition-lists)
* [Subscript and superscript](#subscript-and-superscript)
* [Math markup with MathJax](#math-markup-with-mathjax)
* [Syntax highlighting and fenced code blocks](#code-blocks)

We've also modified the following aspects of standard Markdown behaviour:

* [Line breaks from new lines](#line-breaks)
* [Inline HTML](#inline-html)
* [Automatic linking](#automatic-linking)
* [Underscores in the middle of a word](#italics)

We've tried to keep the formatting style as simple, concise and readable as possible, while still allowing for a wide range of formatting options. Elements have been borrowed from [GitHub Flavored Markdown (GFM)](http://github.github.com/github-flavored-markdown/) and [StackOverflow's Markdown](http://stackoverflow.com/editing-help), and some of the additional features were inspired by what was available on our MediaWiki site. Below you can find a fairly comprehensive listing of the components of Wikinotes Markdown, but if there's something you're not sure about, don't hestitate to [shoot us an email](/about#contact-us).

You can find the source of our Markdown parser (which uses the python-markdown library and several extensions) in our [GitHub repository](https://github.com/dellsystem/wikinotes/blob/master/wiki/templatetags/wikinotes_markup.py). The markdown source for this page can be found [within the repository](https://github.com/dellsystem/wikinotes/blob/master/wiki/templates/help/formatting.md) as well.

[TOC]

# Inline elements

## Emphasis

### Bold

To make a section of text **bold**, simply put two asterisks or two underscore characters around it, as in the following:

	**this will be bold**
	__this will also be bold__

If you want to enter two asterisks or two underscore characters _without_ bolding anything, you can escape them. For example, `\*\*` will produce \*\*, and `\_\_` will produce \_\_.

### Italics

To _italicise_ a section of text, simply put one asterisk or one underscore character on each side of it, as in the following:

	*this will be italicised*
	_this will be italicised_

As before, entering one underscore or one asterisk can be done by escaping it with the backslash character. `\*` becomes \* and `\_` becomes \_. Alternatively, surround them with spaces: ` * ` or ` _ `.

Underscores in the middle of a word (e.g. some_variable or this_should_work) will not be treated as emphasis. This differs from standard markdown, but is the default behaviour of the python-markdown library as well as GFM.

### Underline

Markdown does not support underlining, mainly because that could cause underlined words to be confused with hyperlinks, and we don't plan on adding it.

## Links

### Standard links

Use `[text to display](http://www.example.com)` to link to something. Relative links work as well; for example, [this](#standard-links) is an anchor link to this section and [this](/help/formatting) is a link to this page, relative to the base of this site. You can also add a title attribute (i.e. the text that appears when you hover over a link) by enclosing it within double quotes at the end of the link: `[text to display](http://www.example.com "This is title text")`.

Make sure to include the `http://` (or whatever protocol it is) when linking to something off-site.

### Reference-style links

Standard Markdown has support for reference-style links, e.g. `[text to display][some link]` where `[some link]` is defined later on in the document, like this:

	:::python
	[some link]: http://www.example.com

We don't encourage the use of this style except in cases where it really offers an improvement. You can learn more about this [here](http://daringfireball.net/projects/markdown/syntax#link).

### Automatic linking

If you just enter http://www.example.com it will automatically link it. Same with www.example.com, www.wikinotes.ca/help, and other such obvious links. If a URL isn't automatically linked, you can of course use the standard link feature mentioned above. The [urlize](https://github.com/r0wb0t/markdown-urlize) Markdown extension is used for this.

## Images

### Image syntax

The syntax is similar to the link syntax, except with a ! at the front:

	![Alt text](http://beta.wikinotes.ca/static/img/logo.png "Title text")

will produce

![Alt text](http://beta.wikinotes.ca/static/img/logo.png "Title text")

The alt text must be specified, although it can be left empty if so desired. The title text is optional.

### Policy on outside images

If you find an image that you want to incorporate into a page, please first make sure that you have permission to use it, and check for license compatibility. (You can find out more about copyright issues on Wikinotes [here](/help/copyright).) We don't recommend hotlinking - we will eventually have an image uploading feature, but until that has been created we suggest reuploading the image somewhere such as www.imgur.com or your cs.mcgill.ca website if you have one.

## Inline code

The syntax is the same as in [standard Markdown](http://daringfireball.net/projects/markdown/syntax#code) - just use backticks (\`) to enclose inline code. For example, `some_function_name()`.  To enter a backtick by itself, escape it: \`. To enter a single backtick within inline code, you can use multiple backticks as the delimiters.

## Subscript and superscript

Subscript is just ~this~. Superscript is ^this^. Syntax:

	CO~2~ for subscript
	E=mc^2^ for superscript

We use the [subscript](https://github.com/sgraber/markdown.subscript) and [superscript](https://github.com/sgraber/markdown.superscript) extensions written by Shane Graber for this.

If you need to write mathematical expressions, it is preferred that you use [LaTeX math markup](#math-markup), which will be processed by MathJax and converted into beautifully typeset math.

# Block elements

## Headers

### Header syntax

Like `# Header text` or `## Header text`, all the way up to five `#`'s. The space is not necessary (`#Header text` would work, for example) and you can place the same number of `#`'s on the other side as well, but for cleanness as consistency, we recommend the syntax above. We also prefer that only the first word be capitalised.

### Alternative syntax

The following Setext-style syntax for top-level and second-level headers would work as well:

	:::python
	Test
	----
	Test
	====

However, we prefer the [aforementioned](#header-syntax) Atx-style headers because they have a wider range and necessitate fewer characters.

### Section numbers

Automatic section numbering is automatic. You can't disable it. Sorry.

### Mapping to HTML headers

Typically, a `# Header` will become `<h1>Header</h1>`, `## Header` will become `<h2>Header</h2>`, and so on. However, we use the [downheader](http://code.google.com/p/markdown-downheader/) Markdown extension to convert `# Header` into `<h2>Header</h2>`, etc (with the smallest header being `##### Header`, an `<h6>` element). This is because having more than one h1 element on a page doesn't make much sense, semantically.

## Paragraphs

Surround a block of text with empty lines (or just nothing) before and after it and bam, paragraph.

## Tables

### Creating a table

A basic example:

	Header cell 1 | Header cell 2
	------------- | -------------
	Content cell 1 | Content cell 2
	Content cell 3 | Content cell 4

becomes

Header cell 1 | Header cell 2
------------- | -------------
Content cell 1 | Content cell 2
Content cell 3 | Content cell 4

The pipe (|) characters don't have to be lined up. It's also possible to put the pipes on the outside as well, although this is not necessary:

	|Header cell 1 | Header cell 2|
	|------------- | -------------|
	|Content cell 1 | Content cell 2|
	|Content cell 3 | Content cell 4|

### Column alignment

You can align individual columns using a colon (:) to indicate the direction of alignment. For example:

Right alignment | Left alignment | Center alignment
---------------:|:---------------|:---------------:
Content cell 1  | Content cell 2 | Content cell 3
Content cell 4  | Content cell 4 | Content cell 6

### Allowing sorting

By default, tables can not be sorted. If you want a table to be sortable via the [jQuery tablesorter plugin](http://tablesorter.com/docs/), add the "sort" class to it, like this:

	Header cell 1 | Header cell 2
	------------- | ------------- sort
	Content cell 1 | Content cell 2
	Content cell 3 | Content cell 4

which will result in a table whose rows are sortable by the cell values per column, by clicking on the column headers:

Header cell 1 | Header cell 2
------------- | ------------- sort
Content cell 1 | Content cell 2
Content cell 3 | Content cell 4

### Changing the colour scheme

Besides the "sort" class, the following classes can be placed at the end of the second line in a table, separated by a space:

* clear
* autumn
* lights
* fresh
* ribbon
* iris

These all indicate colour schemes for the tables. The `autumn` colour scheme looks as follows:

Header cell 1 | Header cell 2
------------- | ------------- autumn
Content cell 1 | Content cell 2
Content cell 3 | Content cell 4

You can specify multiple colour schemes (or add the `sort` attribute) for one table by separating them with spaces, although it might not turn out the way you want. Still, feel free to experiment.

## Blockquotes

Same as in [regular markdown](http://daringfireball.net/projects/markdown/syntax#blockquote). You can nest them, and add other block elements as well. For example:

	> This is a blockquote
	> This is the second line
	>
	> > This is a nested blockquote
	>
	> Back to the original blockquote

will render as

> This is a blockquote
> This is the second line
>
> > This is a nested blockquote
>
> Back to the original blockquote

## Lists

Same as in [standard markdown](http://daringfireball.net/projects/markdown/syntax#list). To create an unordered list, you can use \*, +, or - as the list delimiters. For example:

	* List item one
	* List item two
	* List item spanning
	multiple lines
	* Last list item

becomes

* List item one
* List item two
* List item spanning
multiple lines
* Last list item

You can create ordered lists simply by numbering your list items. The numbers don't have to be in order, but it's probably better if they are. For example:

	1. List item one
	2. List item two
	3. List item spanning
	multiple lines
	4. Last list item

becomes

1. List item one
2. List item two
3. List item spanning
multiple lines
4. Last list item

## Code blocks

### Tabbed code blocks

As in [standard Markdown](http://daringfireball.net/projects/markdown/syntax#precode), you can create a code block by indenting each line with four spaces or a tab. Relative indentation is preserved, and you shouldn't need to escape anything (HTML- and Markdown-specific special characters are converted automatically, for example).

### Fenced code blocks

You can also create fenced code blocks, which allow you to insert code as above but without having to manually indent anything. Just wrap the block with 3 backtick characters or 3 tilde characters. For example:

	```
	def some_function(some_param):
		some_var = some_param > 0
		do_something(some_var)
	```

We use the [fenced code blocks](http://freewisdom.org/projects/python-markdown/Fenced_Code_Blocks) extension found in the standard Markdown library, with some modifications to make it more similar to GFM.

### Syntax highlighting

We use Pygments and a modified version of the [CodeHilite](http://freewisdom.org/projects/python-markdown/CodeHilite) extension to provide syntax highlighting for tabbed or fenced code. You can set the language in several ways depending on whether you use tabbing or fencing for your code block. For example:

	```python
	def some_function(some_param):
		some_var = some_param > 0
		do_something(some_var)
	```

and

		:::
		:::python
		def some_function(some_param):
			some_var = some_param > 0
			do_something(some_var)

will direct Pygments to use Python as the highlighting language, which will appear as follows:

```python
def some_function(some_param):
	some_var = some_param > 0
	do_something(some_var)
```

You can also set the language by including a [shebang](http://en.wikipedia.org/wiki/Shebang_(Unix)) line at the beginning of the code block:

```
	:::
	#!/usr/bin/python
	def some_function(some_param):
		some_var = some_param > 0
		do_something(some_var)
```

will result in

	#!/usr/bin/python
	def some_function(some_param):
		some_var = some_param > 0
		do_something(some_var)

Including a shebang line will always trigger the appearance of line numbers, although you can get around them by setting the language in another way; see the section on [line numbers](#line-numbers) below for more.

If you don't set the language, Pygments will not try to guess the language, and so the code will appear in one colour.

### Line numbers

If you're going to be discussing a code block on a page, we recommend the use of line numbers. There are four different ways to force line numbers, depending on whether or not you set the language and whether you use tabbing or fencing.

Tabbed, no language set:

```
	:::
	#!
	this is a code block
	spanning multiple lines
```

Fenced, no language set:

	```!
	this is a code block
	spanning multiple lines
	```

Both of the above will result in:

```!
this is a code block
spanning multiple lines
```

Tabbed, language set:

```
	:::
	#python!
	def some_function(some_param):
		some_var = some_param > 0
		do_something(some_var)
```

Fenced, language set:

	```python!
	def some_function(some_param):
		some_var = some_param > 0
		do_something(some_var)
	```

Both of the above will result in:

```python!
def some_function(some_param):
	some_var = some_param > 0
	do_something(some_var)
```

If you want to disable line numbers on a code block that includes the shebang line, simply use `:::` as the first line. You'll have to set the language separately if you want it to be highlighted, though.

## Horizontal rules

You can create a horizontal rule using three or more asterisks, like this:

	***

which will produce

***

See the [standard Markdown documentation on this](http://daringfireball.net/projects/markdown/syntax#hr) for more.

## Definition lists

We use a slightly modified version of the [definition list](http://freewisdom.org/projects/python-markdown/Definition_Lists) extension included with the standard Markdown library. A definition list is contained within a <dl></dl> element, with each term within a <dt></dt> and each definition within a <dd></dd>. An example should suffice:

	term
	: definition
	: another def
	term
	another term
	: a def
	last term
	: definition

turns into

term
: definition
: another def
term
another term
: a def
last term
: definition

Useful for vocabulary lists and the like.

## Footnotes

We use the [footnotes](http://freewisdom.org/projects/python-markdown/Footnotes) extension included in the standard Markdown library to add footnote functionality, similar to that which is available with MediaWiki. Footnotes can be defined using the following syntax:

	This is text[^1^] and more text[^2^]

will become: This is text[^1] and more text[^2]

Although the footnotes will automatically become numbers, you don't need to number them properly, or even use numbers:

	This is text[^lol] and more text[^5]

will show up as: This is text[^lol] and more text[^5].

You can define footnotes at the bottom of the page. (Or rather, anything after the footnotes will be considered part of the footnotes.) Footnote definitions can be multiple lines, with blockquotes, code blocks, and other block elements. Just be sure to indent subsequent lines with an additional four spaces (or tab).

Although failing to define a footnote won't break anything, it may mess up the formatting a bit, so we don't recommend it.

# Miscellaneous

## Line breaks

Same as StackOverflow and GFM. A new line becomes a line break. For example:

	This is a haiku
	Or at least it will be soon
	After this line ends

This is a haiku
Or at least it will be soon
After this line ends

Included as an extension in the standard Markdown library as of version 2.1.0.

## Inline HTML

HTML tags are automatically escaped for security reasons.[^lolwebct] If there's some styling or formatting technique you need that doesn't have an adequate Markdown replacement, please [let us know](/about#contact-us).

## Math markup

We use [MathJax](http://www.mathjax.org/) for client-side processing of LaTeX math markup. There is a fairly useful list on [Wikipedia](http://en.wikipedia.org/wiki/Help:Displaying_a_formula) of the most common symbols and expressions. Instead of <math></math> tags, we use the dollar sign - \$ for inline, \$\$ for display. For example:

	This is text $a^2 + b^2 = c^2$ and that was the Pythagorean theorem.

will turn into

This is text $a^2 + b^2 = c^2$ and that was the Pythagorean theorem.

For display math, which will be horizontally centered on the page, use two \$'s. For example:

	This is text

	$$\sqrt{a^2 + b^2 = c^2}$$

	That was centered

will be rendered as

This is text

$$\sqrt{a^2 + b^2 = c^2}$$

That was centered

You can also force display-style math within inline math. For example, `$\int_x^{\infty}$` displays as $\int_x^{\infty}$, but if you add `\displaystyle` to the beginning of the expression, it appears instead as $\displaystyle \int_x^{\infty}$

To insert a \$ without meaning for it to delimit math, escape it, like this: `\$`

## Escaping things

Most special characters can be escaped with a backslash. You can find more information in the [Markdown documentation](http://daringfireball.net/projects/markdown/syntax#backslash).

[^1]: lol
[^2]: lol
[^lol]: lol
[^5]: lol
[^lolwebct]: lol
