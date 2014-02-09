from django.shortcuts import render, get_object_or_404

from blog.models import BlogPost
from wiki.utils.decorators import show_object_detail


def main(request):
    data = {
        'title': 'News',
        'blog_posts': BlogPost.objects.order_by('-timestamp').all(),
    }

    return render(request, 'news/main.html', data)


@show_object_detail(BlogPost)
def view(request, post):
    return {
        'title': str(post),
        'post': post,
    }
