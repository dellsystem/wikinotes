from fabric.api import *

def less():
	local("lessc -x assets/css/bootstrap.less > assets/css/bootstrap.css")

def kill():
	# First check if it's running in the first place
	num_processes = int(run('ps aux | grep gunicorn_django | wc -l'))
	if num_processes > 2: # 2 because, the grep and the bash -l process
		run("killall gunicorn_django")

def update():
	run("cd /srv/beta/wikinotes; git pull")

def deploy():
	# Kill the old process
	kill()
	# Pull it, updating the source
	update()
	# Less minification
	run("cd /srv/beta/wikinotes; fab less")
	# Don't need to do collectstatic because it is aliased to assets/ T_T
	# Start running the new one
	run("cd /srv/beta; source bin/activate; cd wikinotes; nohup gunicorn_django --workers=2 >> log &", pty=False)

def broadcast():
	local("python manage.py runserver 0.0.0.0:8000")

def server():
	local("python manage.py runserver --insecure")

def test():
	local("python manage.py test wiki")
