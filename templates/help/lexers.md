Here you can find a list of the more common languages we support syntax highlighting for, as well as some languages which we don't support directly but which can be highlighted using another language's lexer. For some of the languages, you will also find a short code sample for each language, highlighted with the relevant lexer.

To see the entire list of languages, take a look at the [Pygments documentation](http://pygments.org/docs/lexers/).

# Common languages

**Format:**

Name of language
:	short name (i.e. what to enter in the code block to make it highlight; if there are multiple short names, they are separated by a comma, and using any is acceptable)

For example, if the short name were `somelang`, you can select that lexer by doing

	```somelang
	[...]
	```

Bash
:	bash, sh, ksh
Bash session
:	console
C
:	c
C++
:	c++, cpp
CSS
:	css
HTML
:	html
Java
:	java
Javascript
:	js, javascript
Makefile
:	make, makefile, mf, bsdmake[^bsdmake]
MATLAB
:	matlab
MATLAB session
:	matlabsession
MIPS
:	gas[^gas]
PHP
:	php, php3, php4, php5
Python console
:	pycon
Python
:	python, py
Python traceback
:	pytb
Ruby console
:	rbcon, irb
Ruby
:	rb, ruby, duby
SML
:	ocaml[^ocaml]
SQL
:	sql
TeX
:	tex, latex

# Code samples

Later

[^gas]: There is no actual lexer for MIPS, but the [gas lexer](http://en.wikipedia.org/wiki/GNU_Assembler) comes close.
[^bsdmake]: For BSD makefiles.
[^ocaml]: Sadly, there is no lexer for Standard ML. The OCaml lexer comes close, though.
