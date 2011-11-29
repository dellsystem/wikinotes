from django.shortcuts import render
from blog.models import BlogPost

def main(request):
	data = {
		'blog_posts': BlogPost.objects.order_by('-timestamp').all(),
	}
	return render(request, 'news/main.html', data)

def view(request, slug):
	data = {
		'post': BlogPost.objects.get(slug=slug),
	}
	return render(request, 'news/view.html', data)
