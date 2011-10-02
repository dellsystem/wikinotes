![WikiNotes logo](http://www.wikinotes.ca/logo_new.png)

Instructions for testing and development
----------------------------------------

###Dependencies###

* Python 2.6+ (possibly 2.7+, I can't remember)
* Django 1.3+
* pyyaml (`apt-get install python-yaml`)
* python-markdown (`apt-get install python-markdown`), with [this extension](https://github.com/mayoff/python-markdown-mathjax) - download the [mdx_markdown.py](https://raw.github.com/mayoff/python-markdown-mathjax/master/mdx_mathjax.py) file, rename it to mathjax.py, and place it in the extensions directory for your markdown installation. (See the [readme](https://github.com/mayoff/python-markdown-mathjax/blob/master/README.md) for more information.)
* django-gravatar (`pip install django-gravatar`)
* GitPython (`easy_install gitpython`) - may be removed later

###Setup instructions (IMPORTANT)###

* Edit the `wikinotes_dir` variable in settings.py to reflect the absolute path of the directory this is stored in.
* `chmod +x bootstrap; bootstrap` (you should create the superuser at this point if you haven't already done so)
* `python manage.py runserver`
* Go to localhost:8000. Or, if you run it on 0.0.0.0:8000 with `python manage.py runserver 0.0.0.0:8000` (or any other port), others can view it on your IP address.

Things that work or sort of work
--------------------------------

* Creating and editing pages (the icons for creating new pages are just filler) - needs to be improved (better error handling and a nicer input format)
* Browsing all courses (click the Courses menu item), some things on that page (and some linked pages) are just filler though
* User authentication (you can log in using the superuser and any other users you create)
* Gravatar
* Watching a course
* History, some elements
* Random pages

Things that don't really work yet or are in progress (i.e. to-do list)
------------------------------

* Professor field
* Link field
* About, news, help, contributing and other similar static sections (views have not been made yet)
* Search
* Registration (need to merge Clarence's pull request after reviewing it for conflicts etc)
* Recent changes
* 404 page
* UCP (settings etc)
* Dashboard layout
* Icons for page types
* Layouts for editing and presenting page types
* Reverting/rolling back commits, etc
* Get all courses and departments lol
* For all list/table things, check if there is data to show first and include a fallback if there is not

Notes to self (i.e. me, not you)
--------------------------------

* bugs in twitter bootstrap: margins for modals, and that font-weight or line-height or something that i can't find anymore
* make the fullscreen option for section-body work (the 100% - n pixels thing, use divs within a div for that)
* when adding new sections (beyond the initial 10), remember to change the ids, names and <span>n</span>s
* either the "add another section" button or the preview+save buttons are not centered 
* delete icon (top right corner) for sections (like the modal dialogue close icons)
* adding a section should update the number in the num_sections dropdown. actually, lots of bugs in that js, fix that
* capitalisation of term. it's actually really important
* tabindex lol
* how to handle:
	* multiple "quizzes" (as a past exam type) (or multiple versions of exams)
	* the whole silly department/subject fiasco
	* course numbers with letters etc (solution: make it a CharField, max_length=5, and change the regex in urls.py)
	* form data, needed for the create and edit modes - make it customisable on a PageType level
	* subclassing the user model?
* get rid of inline CSS
* better way of putting js on all course/page-related pages
* Possible to remove the GitPython dependency and just use the HistoryItems to view the history for a page?
	* Also, rewrite the Git class using subprocess or something (anything other than `os.system()` ...)
