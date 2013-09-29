![WikiNotes logo](http://www.wikinotes.ca/static/img/wikinotes.png)

by the WikiNotes team

WikiNotes is a wiki-based note-sharing platform created to facilitate student collaboration. Although it is being created primarily to replace [our old MediaWiki-backed website for McGill students](http://69.28.212.103/), we are releasing the code under the [GPLv3](http://opensource.org/licenses/GPL-3.0) so that non-McGill students (or anyone, really) can benefit from it as well. Although this platform is still currently under heavy development, we are now using it to power our main website at http://www.wikinotes.ca.

Want to find out more about us? Visit our [about page](http://www.wikinotes.ca/about), join our IRC channel (#wikinotes on freenode) or drop us a line at admin@wikinotes.ca.

Contributing
------------

We'd love to have you contribute, whether it be through adding features, filing bug reports, writing tests or whatever takes your fancy. Contributing code is easy - just fork this repository, make your changes, and send us a pull request. To see what needs to be done, check out the [list of outstanding issues](https://github.com/dellsystem/wikinotes/issues) or the [roadmap to BETA](https://github.com/dellsystem/wikinotes/issues/48). If you notice something else that needs to be done, feel free to [open an issue](https://github.com/dellsystem/wikinotes/issues/new) for it.

See also our [development wiki](https://github.com/dellsystem/wikinotes/wiki) for things like what style conventions we use, development notes and how the code is organised.

We're using [Travis](http://travis-ci.org) for continuous integration and Django's unit-testing framework for the tests. Current build status of the master branch: [![Build Status](https://secure.travis-ci.org/dellsystem/wikinotes.png?branch=master)](http://travis-ci.org/dellsystem/wikinotes)

Dependencies
------------

To run it on your local machine, you'll need Python 2.7+, and Git. You'll also need a bunch of Python modules, which be installed with [pip](http://www.pip-installer.org/en/latest/index.html):

```console
pip install -r requirements.txt
```

If you don't have pip, either install it using your system's package manager or make use of [virtualenv](http://www.virtualenv.org/en/latest/index.html) (which is a good idea in any case).

Configuration
-------------

If you're running it for the first time, take note of the following setup instructions:

* `./bootstrap` - create the superuser at this point (you may also wish to run this if any database schema changes have been made since your last pull)
* `python manage.py runserver` (by default, this makes the platform accessible at [http://localhost:8000](http://localhost:8000); add `0.0.0.0:8000` if you want to make it publicly accessible through your IP address)
* To run the unit tests, just do `python manage.py test wiki`
