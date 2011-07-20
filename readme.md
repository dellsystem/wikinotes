![wikinotes](http://www.wikinotes.ca/logo_new.png)

Overview
--------

A prototype for moving wikinotes.ca away from MediaWiki, using a custom-written application using Django as a framework. The database currently being used is SQLite but in production it will be either MySQL or PostgreSQL. The wiki pages will be tracked using git, with each page broken up into multiple "sections", all stored as files. This is intended to reduce the amount of unnecessary data stored for each diff, resulting in more efficient disk space usage.

List of features
----------------

_An incomplete list. More to be added when thought of. Features marked in **bold** are features that must be finished before release; the others can be added later_

*	**Ability to "watch this course" to have actions involving that course appear on your dashboard (akin to Github's "Watch this repository/user" or Twitter's "Follow")**
*	Easily compare, merge/squash, revert commits thanks to git
*	**Course pages are automatically generated, so there's no need to copy and paste a template from a previous course when trying to add a new course (same thing for individual pages)**
*	Better integration of comments with specific sections of pages (for example: a particular question on a past exam)
*	**Markdown <3**
*	Exporting of a document into other formats - PDF, plain text (i.e. markdown), print-friendly HTML, kwordquiz (for select page types)
*	Importing of a document from other formats - Google Docs, Word, Mediawiki, Markdown etc; just upload it or enter the URL and we'll see if it can be used
*	**[MathJax](http://www.mathjax.org) for math typesetting because it's beautiful**
*	Integration with docuum and/or qandora? (to be discussed)
*	Inline-editing
*	Auto-saving every few minutes or so, with the user given the option to recover the unsaved changes
*	Better merging and such in the case of simultaneous editing than Mediawiki (as in, merges will be handled automatically UNLESS two people change the same line; in that case, the second person will be asked to confirm the changes). This actually might not be that easy to implement - to be looked into
*	**Easily upload images and other accompanying media**
*	**Support for definition lists and tables using Markdown**
*	Built-in permission system means that it wouldn't be too difficult to have some users who act as moderators etc

Django apps and relevant models
------------------------

*	wikinotes (the main application)
	*	users
		*	extends the User model in django.contrib.auth; adds the CourseWatcher (many-to-many) model
		*	look into openID for authentication
		*	use email to generate Gravatar
	*	courses
		*	each course is associated with an ID, a department, a number, and a name
		*	each course can have multiple CourseSemesters, each of which is tied to a professor, a course, and a semester
	*	departments
		*	primary key = the short name (e.g. MATH, PHIL etc)
		*	foreign key = faculty
		*	each department also has a "full name" (e.g. Mathematics and Statistics, Computer Science, Biology)
	*	faculties
		*	short name (slug), ID, long name
	*	professors
		*	just name, for now (m2m with CourseSemesters)
		*	might need to add something else later ... department? (assuming static) website?
	*	pages
		*	each page is associated with a CourseSemester (even exam types - the relevant CourseSemester is the semester for which the exam was written)
		*	each page must be of a specific PageType (pre-defined)
		*	the contents of each page are not stored in the database, but rather on the filesystem, with changes tracked using git
		*	as for searching, ElasticSearch seems the best (other possibilities incl. Sphinx, grep, and storing the contents in a database - either the one used by Django or a non-relational one like CouchDB - were considered but ElasticSearch seems to be the best bet)
	*	comments
		*	associated with individual sections of pages
		*	may be replies to other comments
		*	think of ways of archiving outdated comments later
		*	need to store commenter ID (or -1 if anonymous)
	*	history
		*	all the edit history, ever
		*	would be good in a couch but that might be harder to get working with Django, so stick with the relational db for now
		*	needs: the user ID (-1 if anon), the page ID (and possibly the department/class if the page was deleted? think about it), the revisions/commits that are being referred to, the type of action that was performed, etc
		*	this needs more work
*	help (tutorials/guides etc)
*	blog (for news etc, could use an already-written app like biblion or banjo or something)

URL scheme
----------

*	Main page, of course, with either introductory text/videos/etc + search bar if you're logged out, or your dashboard if you're logged in (redirect to the latter perhaps)
*	/<?faculty> (e.g. `/science`) to see all the departments and classes within that faculty
*	/<?department> (e.g. `/MATH`) to see all the classes within that department
*	/<?department>-<?class-number> (e.g. `/MATH-141/` to see class main page (like a disambiguation), which shows you recent changes for that class, as well as a list of pages for that class
*	/<?department>-<?class-number>/<?page-type> (e.g. `/MATH-141/lectures/`) for a list of all pages of that page type
*	/<?department>-<?class-number>/<?term>-<?year> (e.g. `/MATH-141/fall-2011/`) for a list of all pages belonging to that semester
*	/<?department>-<?class-number>/create/<?page-type> (e.g. `/MATH-141/create/lectures/`) to create a new page of that type
*	/<?department>-<?class-number>/<?term>-<?year>/<?page-type>/<?page-slug> (e.g. `/MATH-141/fall-2011/lectures/september-1`) to view a specific page; append /edit to the URL to edit that page
*	/user/<?username> - see that user's gravatar, list of watched classes, things that user has done

To-do list
----------

*	Watch this class button - getJSON or something, returns whether the user is already watching it or not
	*	Also incorporate authentication - if the user is not logged in, redirect to login page or something
*	Make "Find a course" "random course" etc things under the header
*	make faculty images
*	History model (also diffing, merging etc)
*	Escaping backslashes between $$'s on a line and $$$ throughout the entire thing (for mathjax/markdown to work together properly)
*	Editing - possibility of using AJAX to do inline editing? like "quick edit"
*	Refactor code (it's messy and there's too much repetition)
*	When adding a new course semester, make an option to set the prof for that semester? or just make it unknown?
*	Faculty/department templates
*	Comments
*	Security shit
*	Make handling of semesters better. There's too much title() and whatever going on
*	Fallbacks for people who have JS disabled - maybe all the buttons actual links, to actual pages, but disable clicking if JS is enabled for the cooler effects
*	Try to merge some of the models/views/utils etc into one ... faculties and departments are practically the same, for instance
*	Unit tests just do it
*	Fix thing where additional sections aren't counted because num_sections is never updated >_>
*	Correctly list all the pages in the category- and semester-based views
*	More instance methods as opposed to utility methods (when relevant)
*	Make some sort of generic success template (like the whole trigger_error thing in phpBB)
