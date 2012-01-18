from django.shortcuts import render
from blog.models import BlogPost

def main(request):
	data = {
		'title': 'News',
		'blog_posts': BlogPost.objects.order_by('-timestamp').all(),
	}
	return render(request, 'news/main.html', data)

def view(request, slug):
	post = BlogPost.objects.get(slug=slug)
	data = {
		'title': post,
		'post': post,
	}
	return render(request, 'news/view.html', data)
