from fabric.api import local

def less():
    local("lessc -x assets/css/bootstrap.less > assets/css/bootstrap.css")
