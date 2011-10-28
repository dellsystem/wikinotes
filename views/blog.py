from django.shortcuts import render
from blog.test import tes
def show_posts(request):
    #posts = Blog.objects.all()
    data = {'posts' : '' }
    return render(request, 'blog/all_posts.html', data)

def write_post(request):
    return render(request, 'blog/write_post.html')

def register_post(request):
    pass
