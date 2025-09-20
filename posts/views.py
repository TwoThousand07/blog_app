from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotFound
from .models import Post
from .forms import PostForm

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'posts/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    return render(request, 'posts/post_detail.html', {'post': post})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect('post_list')
    
    else:
        form = PostForm()

    return render(request, 'posts/post_create.html', {'form': form})

@login_required
def post_update(request, slug):
    try:

        post = Post.objects.get(slug=slug)

        if post.author == request.user:
            if request.method == "POST":
                form = PostForm(request.POST, instance=post)
                if form.is_valid():
                    form.save()
                    return redirect("post_detail", slug=post.slug)
                return render(request, "posts/post_update.html", {"form": form, "post": post})
            else:
                form = PostForm(instance=post)
                return render(request, 'posts/post_update.html', {'form': form, 'post': post})
        else:
            raise PermissionDenied("You don't have permissions to edit this post.")
    except Post.DoesNotExist:
        return HttpResponseNotFound('<h2>Page not found.</h2>')

def post_delete(request, slug):
    try:
        post = Post.objects.get(slug=slug)

        if post.author == request.user:
            post.delete()
            return redirect('post_list')
        else:
            raise PermissionDenied("You don't have permissions to delete this post.")
    except Post.DoesNotExist:
        return HttpResponseNotFound('<h2>Page not found.</h2>')
