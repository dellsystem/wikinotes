Instructions for testing and development
----------------------------------------

* Make sure you have all the dependencies. The major ones are: python 2.6+ (possibly 2.7+, I can't remember), Django 1.3+, pyyaml, and GitPython.
* Edit the `wikinotes_dir` variable in settings.py to reflect the absolute path of the directory this is stored in.
* `chmod +x bootstrap`
* `./bootstrap`
* `python manage.py runserver`
* Go to localhost:8000. Or, if you run it on 0.0.0.0:8000 (or any other port; `python manage.py runserver 0.0.0.0:8000`), others can view it on your IP address.

Notes
-----

* A lot of views haven't been made yet. If a link appears broken, that's why
* I'm working on making skeleton views for most of the links, though, so it's easier for others to work on things
* The header needs to be changed a bit. It's too much like the twitter bootstrap demo page.

Notes to self (i.e. me, not you)
--------------------------------

* bugs in twitter bootstrap: margins for modals, and that font-weight or line-height or something that i can't find anymore
* make the fullscreen option for section-body work (the 100% - n pixels thing, use divs within a div for that)
* when adding new sections (beyond the initial 10), remember to change the ids, names and <span>n</span>s
* either the "add another section" button or the preview+save buttons are not centered 
* delete icon (top right corner) for sections (like the modal dialogue close icons)
* adding a section should update the number in the num_sections dropdown
* capitalisation of term. it's actually really important
* escaping \ in mathjax (because of markdown etc)
* tabindex
* how to handle:
	* multiple "quizzes" (as a past exam type) (or multiple versions of exams)
	* the whole silly department/subject fiasco
	* course numbers with letters etc
	* form data, needed for the create and edit modes
* move create from courses.py to pages.py because it makes more sense there (easier to reuse code too etc)
