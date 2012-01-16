from fabric.api import local

def less():
    local("lessc assets/css/bootstrap.less > assets/css/bootstrap.css")
