![WikiNotes logo](http://www.wikinotes.ca/logo_new.png)

by the WikiNotes team

WikiNotes is a wiki-based note-sharing platform created to facilitate student collaboration. Although it is being created primarily for use by our [existing website for McGill students](http://www.wikinotes.ca), we will be releasing the code under the [GPLv3](http://opensource.org/licenses/GPL-3.0) so that non-McGill students (or anyone, really) can benefit from it as well. This platform is currently under heavy development, but we're hoping to get a beta up and running by late November - stay tuned.

Want to find out more about us? Visit our [about page](http://www.wikinotes.ca/wiki/wikinotes:About), join our IRC channel (#wikinotes on freenode) or drop us a line at admin@wikinotes.ca.

Contributing
------------

We'd love to have you contribute, whether it be through adding features, filing bug reports, writing tests or whatever takes your fancy. To run it on your local machine, you'll need the following dependencies:

* Python 2.6+ (possibly 2.7+)
* Django 1.3+
* pyyaml (on Debian-based distributions, `apt-get install python-yaml`)
* python-markdown (`apt-get install python-markdown`), with [this extension](https://github.com/mayoff/python-markdown-mathjax) - download the [mdx_markdown.py](https://raw.github.com/mayoff/python-markdown-mathjax/master/mdx_mathjax.py) file, rename it to mathjax.py, and place it in the extensions directory for your markdown installation. (See the [readme](https://github.com/mayoff/python-markdown-mathjax/blob/master/README.md) for more information.)
* django-gravatar (`pip install django-gravatar`)
* GitPython (`easy_install gitpython`)
* Git 1.7+ (older versions may work), both for version control and for the wiki software itself

If you're running it for the first time, take note of the setup instructions:

* `chmod +x bootstrap`
* `./bootstrap` - create the superuser at this point (you may also wish to run this if any database schema changes have been made since your last pull. if that doesn't fix things, delete the db.sqlite file and try again)
* `python manage.py runserver` (by default, this makes the platform accessible at [http://localhost:8000](http://localhost:8000); add `0.0.0.0:8000` if you want to make it publicly accessible through your IP address)
* To run the unit tests, just do `python manage.py test` (there are quite a few tests to run because of all the dependencies, so this may take a while)

Contributing code is easy - just fork this repository, make your changes, and send us a pull request. To see what needs to be done, check out the [list of outstanding issues](https://github.com/dellsystem/wikinotes/issues) or the [roadmap to BETA](https://github.com/dellsystem/wikinotes/issues/48). If you notice something else that needs to be done, feel free to [open an issue](https://github.com/dellsystem/wikinotes/issues/new) for it.

See also our [development wiki](https://github.com/dellsystem/wikinotes/wiki) for things like what style conventions we use, development notes and how the code is organised.
