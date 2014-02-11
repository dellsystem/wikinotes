from fabric.api import *


def less():
    local("lessc -x assets/css/bootstrap.less > assets/css/bootstrap.css")


def broadcast():
    local("python manage.py runserver 0.0.0.0:8000")


def up():
    local("python manage.py runserver --insecure")


def test():
    local("python manage.py test wiki")


def refresh():
    local("python manage.py remarkdown")


def sh():
    local("python manage.py shell")


def backup():
    local("python manage.py dumpdata > backup.json")


def restart():
    local("kill -HUP `cat /tmp/gunicorn.pid`")
