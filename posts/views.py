from django.shortcuts import render, get_object_or_404
from django.http import Http404

from .models import Post

def home_view(request):
    return render(request, 'base.html', {'title': 'Blog'})

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'posts/post_list.html', {'posts': posts})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)

    return render(request, 'posts/post_detail.html', {'post': post})

