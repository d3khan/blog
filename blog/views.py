
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Post
from .forms import PostForm

def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})

def submit_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            # Send email notification
            subject = f'New Blog Post: {post.title}'
            body = f"""
A new blog post has been submitted!

Title: {post.title}
Author: {post.author}
Category: {post.category}
Email: {post.email}
Date: {post.created_at}

Content:
{post.content}

View at: http://127.0.0.1:8000/admin/blog/post/{post.id}/change/
"""
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL or 'noreply@d3khan.blog',
                [settings.NOTIFY_EMAIL],
                fail_silently=False,
            )
            messages.success(request, 'Your post has been submitted and an email notification was sent!')
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})
