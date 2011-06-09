Wikinotes prototype
==================

Using Django as a framework. SQLite in development but either MySQL or PostgreSQL as a database. It's going to be fucking awesome.

Apps
---------

*	users - each user is associated with the following data:
	*	username
	*	user ID
	*	email (which can be used to generate a gravatar)
	*	a list of classes (IDs) that the user is watching
	*	look into openID for authentication? if there is a django-openID bridge thing
*	classes - each class is associated with the following data:
	*	class ID
	*	department ID (see below)
	*	class number (for MATH 133, it would be 133)
	*	class name (e.g. Linear Algebra or Introduction to Computing)
*	departments
	*	department ID
	*	department short name (e.g. MATH, PHIL, etc)
	*	department full name (e.g. Mathematics and Statistics, Computer Science, Biology)
	*	faculty (Science, Arts, Engineering etc)
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
*	help - maybe general tips and stuff, also some specific to each section of the site
*	static
*	history - all the edit history, ever. this would be good in a couch.
	*	user ID (the user who did the thing)
	*	class ID (the class for which the thing was done)
	*	if the thing was page-related:
		*	the page ID
		*	the revision number of the original page if it was edit or rollback or something
		*	if it was move or create or delete, then we don't need the revision number
	*	if the thing was document-uploading-related:
		*	the document ID on docuum ?
		*	the document name

Features/functionalities to include
-----------------------------------

*	Attachments - images, tables, etc should be easily uploaded/created and easily attached to a post
	*	Maybe use couchDB for that too even
*	integration with docuum and/or qandora?
*	mathjax for math processing would be stellar
*	markdown (python library) for other stuff
*	easily convert from google docs, word etc formats: upload/add url, we'll convert to markdown
*	easily export to other formats: PDF, plain text (markdown lol), kwordquiz (for select pages)

To-do list
----------

*	get started lol
