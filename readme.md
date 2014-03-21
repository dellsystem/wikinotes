![WikiNotes logo](http://www.wikinotes.ca/static/img/wikinotes.png)

WikiNotes is a wiki-based note-sharing platform created to facilitate student
collaboration. Although it is being created primarily to replace our old
MediaWiki-backed website for McGill students, we are releasing the code under
the [GPLv3][gpl] so that non-McGill students (or anyone, really) can benefit
from it as well. Although this platform is still under development, we are now
using it to power our main website at www.wikinotes.ca.

Want to find out more about us? Visit our [about page][about], join our IRC
channel ([#wikinotes on freenode][irc]) or drop us a line at
<admin@wikinotes.ca>.

Contributing
------------

We'd love to have you contribute, whether it be through adding features, filing
bug reports, writing tests or whatever takes your fancy. Contributing code is
easy - just fork this repository, make your changes, and send us a pull request.
To see what needs to be done, check out the [list of outstanding
issues][issues]. If you notice something else that needs to be done, feel free
to [open an issue][open] for it.

See also our [development wiki][wiki] for things like what style conventions we
use, development notes, and how the code is organised.

We're using [Travis][travis] for continuous integration and Django's
unit-testing framework for the tests. Current build status of the master branch:

[![Build status][status]][ci]

Dependencies
------------

To run it on your local machine, you'll need Python 2.7+, and Git. If you're on
Windows, you might run into some issues which I won't be able to help debug, so
I'd recommend using Linux if possible. You'll also need a bunch of Python
modules, which can be installed with [pip]:

```console
pip install -r requirements.txt
```

If you don't have pip, either install it using your system's package manager or
make use of [virtualenv] \(which is a good idea in any case\).

Configuration
-------------

If you're running it for the first time, here's what you have to do:

* Run `python manage.py syncdb`. Make sure to create the superuser when
  prompted. You will be able to use the credentials you choose for the
  superuser account to log on to the site, and to access the administration
  panel.
* Run `python manage.py runserver` (or `fab up` if you have [Fabric][fabric]
  installed) to start the development server. By default, this makes the
  platform accessible at <http://localhost:8000>; add `0.0.0.0:8000` as an
  argument if you want to make it publicly accessible through your IP address
  (at port 8000), or run `fab broadcast`. To actually deploy it properly on a
  server, you'll probably want to use something like [gunicorn].

Initially, there won't be any courses on the site. You can create them through
the admin panel (sign in using the superuser account details through the login
box in the header, then click the "admin" button), or write a script to import
them if you have a list of all the courses/departments/faculties to create.

If you have questions, send me an email (ilostwaldo, gmail).

Testing
-------

To run the unit tests, run `python manage.py test wiki` or `fab test`. You can
view the history of the tests run for commits pushed to the master branch on
[Travis][ci].

[gpl]: http://opensource.org/licenses/GPL-3.0
[about]: http://www.wikinotes.ca/about
[irc]: http://webchat.freenode.net/?channels=wikinotes
[issues]: https://github.com/dellsystem/wikinotes/issues
[open]: https://github.com/dellsystem/wikinotes/issues/new
[wiki]: https://github.com/dellsystem/wikinotes/wiki
[travis]: http://travis-ci.org
[status]: https://secure.travis-ci.org/dellsystem/wikinotes.png?branch=master
[ci]: http://travis-ci.org/dellsystem/wikinotes
[pip]: http://www.pip-installer.org/en/latest/index.html
[virtualenv]: http://www.virtualenv.org/en/latest/index.html
[fabric]: http://fabfile.org
[gunicorn]: https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/gunicorn/
