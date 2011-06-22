Wikinotes prototype
==================

Using Django as a framework. SQLite in development but either MySQL or PostgreSQL as a database. The wiki pages will be tracked using git, with each page broken up until multiple "sections", all stored as files. This is intended to reduce the amount of unnecessary data stored for each diff, resulting in more efficient disk space usage.

Apps and relevant models
---------

*	wikinotes
	*	users - each user is associated with the following data:
		*	username
		*	user ID
		*	email (which can be used to generate a gravatar)
		*	a list of classes (IDs) that the user is watching
		*	look into openID for authentication? if there is a django-openID bridge thing
		*	but rely on django's authentication module for most of the user data (username, user ID, email) - only the CourseWatcher model needs to be custom
	*	courses - each course is associated with the following data:
		*	course ID
		*	department shortname (see below)
		*	course number (for MATH 133, it would be 133)
		*	course name (e.g. Linear Algebra or Introduction to Computing)
	*	departments
		*	department short name (e.g. MATH, PHIL, etc)
		*	department full name (e.g. Mathematics and Statistics, Computer Science, Biology)
		*	faculty (Science, Arts, Engineering etc)
	*	faculties
		*	faculty short name
		*	faculty ID (or maybe the short name should be the pk)
		*	faculty long name
	*	professors
		*	name, for now (m2m with CourseSemesters)
	*	pages - this is where using either git or CouchDB would come in handy
		*	page ID, maybe store that in the relational database (not sure if it's even necessary)
		*	class ID (the class it is associated with)
		*	revision number
		*	page type: description/lecture note/summary/review/etc
		*	page content ... git/couchDB
	*	comments - like a talk page, but associated with individual pages
		*	comment ID
		*	page ID (foreign key)
		*	commenter ID (foreign key, users table - if -1, anonymous)
		*	comment content
		*	revision number it refers to
	*	history - all the edit history, ever. this would be good in a couch.
		*	user ID (the user who did the thing)
		*	class ID (the class for which the thing was done)
		*	if the thing was page-related:
			*	the page ID
			*	the revision number of the original page if it was edit or rollback or something
			*	if it was move or create or delete, then we don't need the revision number
		*	if the thing was document-uploading-related:
			*	the document ID on docuum ? or wherever
			*	the document name
*	help - maybe general tips and stuff, also some specific to each section of the site

URL scheme
----------

*	Main page, of course, with either introductory text/videos/etc + search bar if you're logged out, or your dashboard if you're logged in (redirect to the latter perhaps)
*	/user/<?username> - see that user's gravatar, list of watched classes, things that user has done
*	/<?department>-<?class-number> (e.g. `/MATH-141/` to see class main page (like a disambiguation), which shows you recent changes for that class, as well as a list of pages for that class
*	/<?department> (e.g. `/MATH`) to see all the classes within that department
*	/<?faculty> (e.g. `/science`) to see all the departments and classes within that faculty
*	/<?department>-<?class-number>/<?page-type> (e.g. `/MATH-141/lectures/`) for a list of all pages of that page type (page types to be decided later)

Features/functionalities to include
-----------------------------------

*	integration with docuum and/or qandora?
*	easily convert from google docs, word, mediawiki etc formats: upload/add url, we'll convert to markdown (or even, upload your own markdown file, we'll check if it's valid)
*	easily export to other formats: PDF, plain text (markdown lol), kwordquiz (for select pages)

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
