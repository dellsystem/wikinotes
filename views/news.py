from django.shortcuts import render, get_object_or_404

from blog.models import BlogPost


def main(request):
    data = {
        'title': 'News',
        'blog_posts': BlogPost.objects.order_by('-timestamp').all(),
    }

    return render(request, 'news/main.html', data)


def view(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    data = {
        'title': post,
        'post': post,
    }

    return render(request, 'news/view.html', data)
