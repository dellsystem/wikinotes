from fabric.api import *

def beta():
	env.hosts = ['deploy@beta.wikinotes.ca']

def less():
	local("lessc -x assets/css/bootstrap.less > assets/css/bootstrap.css")

def kill():
	run("kill $(ps aux | grep gunicorn | awk '{ print $2 }' | sort -nr | tail -n 1)")

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
	run("cd /srv/beta; source bin/activate; cd wikinotes; nohup gunicorn_django --workers=2 >> log &")
