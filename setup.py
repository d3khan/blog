#!/usr/bin/env python3
"""
D3KHAN BLOG - FULL SETUP SCRIPT
Creates Django project with venv in CURRENT folder.
Usage: python setup.py
"""
import os
import sys
import subprocess
import shutil

def run(cmd_list):
    """Run a command list (avoids shell parsing issues with spaces)."""
    cmd_str = " ".join(f'"{x}"' if " " in x else x for x in cmd_list)
    print(f"  $ {cmd_str}")
    result = subprocess.run(cmd_list, capture_output=False, text=True)
    if result.returncode != 0:
        print(f"ERROR: Command failed: {cmd_str}")
        sys.exit(1)
    return result

def main():
    print("=" * 50)
    print("  D3Khan Blog - Django Setup Script")
    print("=" * 50)
    print()
    if sys.version_info < (3, 10):
        print("ERROR: Python 3.10+ required.")
        sys.exit(1)
    print(f"Found Python: {sys.version.split()[0]}")
    abs_path = os.path.abspath(".")
    print(f"Project directory: {abs_path}")
    print()
    print("[1/7] Creating virtual environment venv...")
    run([sys.executable, "-m", "venv", "venv"])
    if os.name == "nt":
        pip = os.path.join(abs_path, "venv", "Scripts", "pip.exe")
        python = os.path.join(abs_path, "venv", "Scripts", "python.exe")
    else:
        pip = os.path.join(abs_path, "venv", "bin", "pip")
        python = os.path.join(abs_path, "venv", "bin", "python")
    run([python, "-m", "pip", "install", "--upgrade", "pip"])
    run([python, "-m", "pip", "install", "Django>=4.2,<5.0"])
    print("Django installed.")
    print()
    print("[2/7] Creating Django project and app...")
    run([python, "-m", "django", "startproject", "d3khan_blog", "."])
    run([python, "manage.py", "startapp", "blog"])
    print()
    print("[3/7] Writing all project files...")
    os.makedirs("blog/management/commands", exist_ok=True)
    os.makedirs("templates/blog", exist_ok=True)
    os.makedirs("static/css", exist_ok=True)
    os.makedirs("static/js", exist_ok=True)

    settings_py = '''
"""Django settings for d3khan_blog."""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-d3khan-blog-2024-change-in-production'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'd3khan_blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'd3khan_blog.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email: console backend for dev (prints to terminal)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# PRODUCTION: Uncomment and configure SMTP below
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = "your-email@gmail.com"
# EMAIL_HOST_PASSWORD = "your-app-password"
# DEFAULT_FROM_EMAIL = "your-email@gmail.com"

NOTIFY_EMAIL = 'd3khan2.0@gmail.com'
'''
    with open("d3khan_blog/settings.py", "w", encoding="utf-8") as fh:
        fh.write(settings_py)
    print("    Created: d3khan_blog/settings.py")

    urls_py = '''
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
'''
    with open("d3khan_blog/urls.py", "w", encoding="utf-8") as fh:
        fh.write(urls_py)
    print("    Created: d3khan_blog/urls.py")

    models_py = '''
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100, blank=True, default='Anonymous')
    category = models.CharField(max_length=50, blank=True, default='General')
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_placeholder = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
'''
    with open("blog/models.py", "w", encoding="utf-8") as fh:
        fh.write(models_py)
    print("    Created: blog/models.py")

    forms_py = '''
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'category', 'email']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter post title',
                'class': 'form-input'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your post content here...',
                'rows': 8,
                'class': 'form-textarea'
            }),
            'author': forms.TextInput(attrs={
                'placeholder': 'Your name (optional)',
                'class': 'form-input'
            }),
            'category': forms.TextInput(attrs={
                'placeholder': 'e.g. Tutorial, Tech, Life',
                'class': 'form-input'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'your@email.com (optional)',
                'class': 'form-input'
            }),
        }
        labels = {
            'title': 'Post Title',
            'content': 'Post Content',
            'author': 'Author Name',
            'category': 'Category',
            'email': 'Email Address',
        }
'''
    with open("blog/forms.py", "w", encoding="utf-8") as fh:
        fh.write(forms_py)
    print("    Created: blog/forms.py")

    views_py = '''
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
'''
    with open("blog/views.py", "w", encoding="utf-8") as fh:
        fh.write(views_py)
    print("    Created: blog/views.py")

    blog_urls_py = '''
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit/', views.submit_post, name='submit_post'),
]
'''
    with open("blog/urls.py", "w", encoding="utf-8") as fh:
        fh.write(blog_urls_py)
    print("    Created: blog/urls.py")

    admin_py = '''
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'created_at', 'is_placeholder']
    list_filter = ['category', 'is_placeholder', 'created_at']
    search_fields = ['title', 'content', 'author']
    date_hierarchy = 'created_at'
'''
    with open("blog/admin.py", "w", encoding="utf-8") as fh:
        fh.write(admin_py)
    print("    Created: blog/admin.py")

    apps_py = '''
from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
'''
    with open("blog/apps.py", "w", encoding="utf-8") as fh:
        fh.write(apps_py)
    print("    Created: blog/apps.py")

    with open("blog/management/__init__.py", "w", encoding="utf-8") as fh:
        fh.write("")
    print("    Created: blog/management/__init__.py")
    with open("blog/management/commands/__init__.py", "w", encoding="utf-8") as fh:
        fh.write("")
    print("    Created: blog/management/commands/__init__.py")

    seed_py = '''
from django.core.management.base import BaseCommand
from blog.models import Post

class Command(BaseCommand):
    help = 'Seed the database with 4 placeholder posts'

    def handle(self, *args, **kwargs):
        placeholders = [
            {
                'title': 'Getting Started with Modern Web Development',
                'content': 'The web development landscape has evolved dramatically over the past decade. From simple HTML pages to complex single-page applications, the tools and frameworks available today empower developers to build incredible experiences. In this post, we explore the essential technologies every modern developer should know: HTML5 semantic elements, CSS Grid and Flexbox, JavaScript ES6+ features, and the rise of progressive web apps. Whether you are just starting out or looking to refresh your skills, understanding these fundamentals will set you up for success in any web project.',
                'author': 'Alex Chen',
                'category': 'Tutorial',
            },
            {
                'title': 'The Art of Clean Code: Best Practices',
                'content': 'Writing clean code is not just about making your programs work—it is about making them work well for everyone who reads them. Clean code is readable, maintainable, and testable. Key principles include meaningful naming conventions, keeping functions small and focused, avoiding unnecessary comments by writing self-documenting code, and following the DRY (Do Not Repeat Yourself) principle. Remember: code is read far more often than it is written. Invest time in clarity, and your future self (and your teammates) will thank you.',
                'author': 'Sarah Miller',
                'category': 'Engineering',
            },
            {
                'title': 'Understanding Async JavaScript',
                'content': 'Asynchronous programming is at the heart of modern JavaScript. From callbacks to promises and now async/await, the language has continuously improved how we handle operations that take time. This post dives deep into the event loop, microtasks, macrotasks, and how JavaScript manages concurrency despite being single-threaded. We will look at practical examples of fetching data from APIs, handling errors gracefully, and avoiding common pitfalls like callback hell or unhandled promise rejections. Mastering async patterns is essential for building responsive web applications.',
                'author': 'Marcus Johnson',
                'category': 'JavaScript',
            },
            {
                'title': 'Design Systems: Building for Scale',
                'content': 'A design system is more than a style guide—it is a comprehensive set of standards, components, and patterns that help teams build consistent user interfaces at scale. Companies like Google (Material Design), IBM (Carbon), and Atlassian have pioneered how design systems drive product consistency and development velocity. This article covers the core elements of a design system: design tokens for colors and typography, reusable UI components, accessibility guidelines, and documentation. We also discuss how to introduce a design system to your organization and measure its impact on product quality and team collaboration.',
                'author': 'Emily Rodriguez',
                'category': 'Design',
            },
        ]

        for data in placeholders:
            Post.objects.get_or_create(
                title=data['title'],
                defaults={
                    'content': data['content'],
                    'author': data['author'],
                    'category': data['category'],
                    'is_placeholder': True,
                }
            )
        self.stdout.write(self.style.SUCCESS('Successfully seeded 4 placeholder posts!'))
'''
    with open("blog/management/commands/seed_posts.py", "w", encoding="utf-8") as fh:
        fh.write(seed_py)
    print("    Created: blog/management/commands/seed_posts.py")

    base_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}D3Khan Blog{% endblock %}</title>
  {% load static %}
  <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>

  <header>
    <div class="header-container">
      <a href="{% url 'home' %}" class="logo">D3<span>Khan</span> Blog</a>
      <a href="{% url 'submit_post' %}" class="post-btn">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/>
        </svg>
        Submit Post
      </a>
    </div>
  </header>

  <main class="container">
    {% if messages %}
      <div class="messages">
        {% for message in messages %}
          <div class="alert alert-{{ message.tags }}">{{ message }}</div>
        {% endfor %}
      </div>
    {% endif %}

    {% block content %}{% endblock %}
  </main>

  <footer>
    <p> D3Khan Blog. Built with Django.</p>
  </footer>

</body>
</html>
'''
    with open("templates/base.html", "w", encoding="utf-8") as fh:
        fh.write(base_html)
    print("    Created: templates/base.html")

    index_html = '''
{% extends 'base.html' %}
{% load static %}

{% block content %}

<div class="blog-intro">
  <h2>Welcome to the Blog</h2>
  <p>Share your thoughts, ideas, and stories. Click "Submit Post" above to contribute!</p>
</div>

<div class="posts-grid">
  {% for post in posts %}
    <article class="post-card {% if not post.is_placeholder %}new{% endif %}">
      <span class="post-badge">{{ post.category|default:"General" }}</span>
      <h3>{{ post.title }}</h3>
      <div class="post-meta">
        <span>
          <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
          </svg>
          {{ post.author|default:"Anonymous" }}
        </span>
        <span>
          <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
          </svg>
          {{ post.created_at|date:"F j, Y" }}
        </span>
      </div>
      <div class="post-content">
        <p>{{ post.content }}</p>
      </div>
    </article>
  {% empty %}
    <div class="loading">
      <div class="spinner"></div>
      No posts yet. Be the first to submit!
    </div>
  {% endfor %}
</div>

{% endblock %}
'''
    with open("templates/blog/index.html", "w", encoding="utf-8") as fh:
        fh.write(index_html)
    print("    Created: templates/blog/index.html")

    form_html = '''
{% extends 'base.html' %}
{% load static %}

{% block title %}Submit a Post - D3Khan Blog{% endblock %}

{% block content %}

<div class="form-page">
  <div class="form-header">
    <div class="form-header-top"></div>
    <div class="form-header-content">
      <h1>Submit a Blog Post</h1>
      <p class="form-subtitle">Share your thoughts with the community. All fields marked with * are required.</p>
    </div>
  </div>

  <form method="post" class="google-form" novalidate>
    {% csrf_token %}

    <div class="form-section">
      <div class="form-field">
        <label for="id_title" class="field-label">
          Post Title <span class="required">*</span>
        </label>
        <div class="field-help">Give your post a clear, descriptive title</div>
        {{ form.title }}
        {% if form.title.errors %}
          <div class="field-error">{{ form.title.errors.0 }}</div>
        {% endif %}
      </div>

      <div class="form-field">
        <label for="id_content" class="field-label">
          Post Content <span class="required">*</span>
        </label>
        <div class="field-help">Write your full post content here</div>
        {{ form.content }}
        {% if form.content.errors %}
          <div class="field-error">{{ form.content.errors.0 }}</div>
        {% endif %}
      </div>

      <div class="form-field">
        <label for="id_author" class="field-label">
          Author Name
        </label>
        <div class="field-help">How should we credit you? (optional)</div>
        {{ form.author }}
        {% if form.author.errors %}
          <div class="field-error">{{ form.author.errors.0 }}</div>
        {% endif %}
      </div>

      <div class="form-field">
        <label for="id_category" class="field-label">
          Category
        </label>
        <div class="field-help">e.g. Tutorial, Tech, Life, Opinion (optional)</div>
        {{ form.category }}
        {% if form.category.errors %}
          <div class="field-error">{{ form.category.errors.0 }}</div>
        {% endif %}
      </div>

      <div class="form-field">
        <label for="id_email" class="field-label">
          Email Address
        </label>
        <div class="field-help">We will not share your email publicly (optional)</div>
        {{ form.email }}
        {% if form.email.errors %}
          <div class="field-error">{{ form.email.errors.0 }}</div>
        {% endif %}
      </div>
    </div>

    <div class="form-actions">
      <button type="submit" class="submit-btn">
        <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path d="M5 13l4 4L19 7"/>
        </svg>
        Submit Post
      </button>
      <a href="{% url 'home' %}" class="cancel-btn">Cancel</a>
    </div>
  </form>
</div>

{% endblock %}
'''
    with open("templates/blog/post_form.html", "w", encoding="utf-8") as fh:
        fh.write(form_html)
    print("    Created: templates/blog/post_form.html")

    css_content = '''
/* ============================================
   D3KHAN BLOG - Blue & White Theme
   ============================================ */

:root {
  --primary-blue: #1565c0;
  --dark-blue: #0d47a1;
  --light-blue: #e3f2fd;
  --accent-blue: #42a5f5;
  --bg-blue: #f0f7ff;
  --card-white: #ffffff;
  --text-dark: #1a237e;
  --text-body: #37474f;
  --border-blue: #bbdefb;
  --shadow: rgba(13, 71, 161, 0.08);
  --form-border: #dadce0;
  --form-focus: #1a73e8;
  --form-bg: #f8f9fa;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  background: var(--bg-blue);
  color: var(--text-body);
  line-height: 1.7;
  min-height: 100vh;
}

/* Header */
header {
  background: linear-gradient(135deg, var(--dark-blue) 0%, var(--primary-blue) 100%);
  color: white;
  padding: 2rem 0;
  box-shadow: 0 4px 20px rgba(13, 71, 161, 0.3);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.8rem;
  font-weight: 800;
  letter-spacing: -0.5px;
  color: white;
  text-decoration: none;
}

.logo span {
  color: var(--accent-blue);
}

.post-btn {
  background: white;
  color: var(--primary-blue);
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 50px;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 10px rgba(0,0,0,0.15);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.post-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.2);
  background: var(--light-blue);
}

.post-btn svg {
  width: 18px;
  height: 18px;
}

/* Main Container */
.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
}

/* Messages / Alerts */
.messages {
  margin-bottom: 1.5rem;
}

.alert {
  padding: 1rem 1.25rem;
  border-radius: 12px;
  font-weight: 500;
  margin-bottom: 0.75rem;
}

.alert-success {
  background: #e8f5e9;
  color: #2e7d32;
  border: 1px solid #a5d6a7;
}

.alert-error {
  background: #ffebee;
  color: #c62828;
  border: 1px solid #ef9a9a;
}

/* Blog Intro */
.blog-intro {
  text-align: center;
  margin: 2rem 0 3rem;
  padding: 2rem;
  background: var(--card-white);
  border-radius: 16px;
  border: 1px solid var(--border-blue);
  box-shadow: 0 4px 20px var(--shadow);
}

.blog-intro h2 {
  color: var(--dark-blue);
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.blog-intro p {
  color: var(--text-body);
  font-size: 1rem;
}

/* Posts Grid */
.posts-grid {
  display: grid;
  gap: 1.5rem;
}

/* Post Card */
.post-card {
  background: var(--card-white);
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid var(--border-blue);
  box-shadow: 0 4px 20px var(--shadow);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.post-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(180deg, var(--accent-blue), var(--primary-blue));
  border-radius: 16px 0 0 16px;
}

.post-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(13, 71, 161, 0.15);
  border-color: var(--accent-blue);
}

.post-badge {
  display: inline-block;
  background: var(--light-blue);
  color: var(--primary-blue);
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.75rem;
}

.post-card h3 {
  color: var(--dark-blue);
  font-size: 1.4rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  line-height: 1.3;
}

.post-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.85rem;
  color: #78909c;
}

.post-meta span {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.post-content {
  color: var(--text-body);
  line-height: 1.8;
}

.post-content p {
  margin-bottom: 0.75rem;
}

/* Loading / Empty State */
.loading {
  text-align: center;
  padding: 3rem;
  color: var(--primary-blue);
  font-size: 1.1rem;
  background: var(--card-white);
  border-radius: 16px;
  border: 1px solid var(--border-blue);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-blue);
  border-top-color: var(--primary-blue);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ============================================
   GOOGLE FORM STYLE - Submit Page
   ============================================ */

.form-page {
  max-width: 640px;
  margin: 2rem auto;
}

.form-header {
  background: var(--card-white);
  border-radius: 16px;
  border: 1px solid var(--form-border);
  overflow: hidden;
  margin-bottom: 1rem;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}

.form-header-top {
  height: 10px;
  background: linear-gradient(90deg, var(--dark-blue), var(--primary-blue), var(--accent-blue));
}

.form-header-content {
  padding: 2rem 2rem 1.5rem;
}

.form-header-content h1 {
  font-size: 2rem;
  font-weight: 400;
  color: var(--text-dark);
  margin-bottom: 0.5rem;
  font-family: 'Google Sans', 'Roboto', 'Segoe UI', sans-serif;
}

.form-subtitle {
  color: #5f6368;
  font-size: 0.95rem;
}

/* Google Form Card */
.google-form {
  background: var(--card-white);
  border-radius: 16px;
  border: 1px solid var(--form-border);
  padding: 2rem;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-field {
  background: var(--card-white);
  border-radius: 8px;
  padding: 1.5rem;
  border: 1px solid var(--form-border);
  transition: all 0.2s ease;
}

.form-field:focus-within {
  border-color: var(--form-focus);
  box-shadow: 0 0 0 2px rgba(26, 115, 232, 0.1);
}

.field-label {
  display: block;
  font-size: 1rem;
  font-weight: 500;
  color: var(--text-dark);
  margin-bottom: 0.5rem;
  font-family: 'Google Sans', 'Roboto', 'Segoe UI', sans-serif;
}

.required {
  color: #d93025;
  margin-left: 0.25rem;
}

.field-help {
  font-size: 0.85rem;
  color: #5f6368;
  margin-bottom: 0.75rem;
}

/* Form Inputs - Google Material Style */
.form-input,
.form-textarea {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid var(--form-border);
  border-radius: 8px;
  font-size: 1rem;
  font-family: inherit;
  color: var(--text-dark);
  background: var(--form-bg);
  transition: all 0.2s ease;
  outline: none;
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: #9aa0a6;
}

.form-input:focus,
.form-textarea:focus {
  border-color: var(--form-focus);
  background: white;
  box-shadow: 0 0 0 3px rgba(26, 115, 232, 0.15);
}

.form-textarea {
  resize: vertical;
  min-height: 120px;
}

.field-error {
  color: #d93025;
  font-size: 0.85rem;
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.field-error::before {
  content: '⚠';
}

/* Form Actions */
.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid var(--form-border);
}

.submit-btn {
  background: var(--primary-blue);
  color: white;
  border: none;
  padding: 0.875rem 2rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 2px 8px rgba(21, 101, 192, 0.3);
}

.submit-btn:hover {
  background: var(--dark-blue);
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(21, 101, 192, 0.4);
}

.cancel-btn {
  color: var(--primary-blue);
  text-decoration: none;
  padding: 0.875rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
}

.cancel-btn:hover {
  background: var(--light-blue);
}

/* Footer */
footer {
  text-align: center;
  padding: 2rem;
  margin-top: 3rem;
  color: #78909c;
  font-size: 0.9rem;
  border-top: 1px solid var(--border-blue);
}

footer a {
  color: var(--primary-blue);
  text-decoration: none;
}

/* New Post Animation */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.post-card.new {
  animation: slideIn 0.5s ease forwards;
}

/* Responsive */
@media (max-width: 768px) {
  .header-container {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .post-card,
  .google-form,
  .form-header {
    padding: 1.25rem;
  }
  
  .container {
    padding: 1rem;
  }
  
  .form-page {
    margin: 1rem;
  }
  
  .form-header-content h1 {
    font-size: 1.5rem;
  }
  
  .form-actions {
    flex-direction: column;
  }
}
'''
    with open("static/css/style.css", "w", encoding="utf-8") as fh:
        fh.write(css_content)
    print("    Created: static/css/style.css")

    js_content = '''
// D3Khan Blog - minimal JS
// Form validation enhancements
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('.form-input, .form-textarea');
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.closest('.form-field').style.borderColor = '#1a73e8';
        });
        input.addEventListener('blur', () => {
            input.closest('.form-field').style.borderColor = '#dadce0';
        });
    });
});
'''
    with open("static/js/app.js", "w", encoding="utf-8") as fh:
        fh.write(js_content)
    print("    Created: static/js/app.js")

    print()
    print("[4/7] Creating blog migration...")
    run([python, "manage.py", "makemigrations", "blog"])
    print()
    print("[5/7] Running Django migrations...")
    run([python, "manage.py", "migrate"])
    print()
    print("[6/7] Seeding 4 placeholder posts...")
    run([python, "manage.py", "seed_posts"])
    print()
    print("[7/7] Create admin superuser? (optional - needed for /admin/)")
    create_admin = input("Create superuser now? (y/n): ").strip().lower()
    if create_admin == "y":
        run([python, "manage.py", "createsuperuser"])
    print()
    print("=" * 50)
    print("  SETUP COMPLETE!")
    print("=" * 50)
    print()
    print(f"Project location: {abs_path}")
    print()
    print("To start the server:")
    if os.name == "nt":
        print("  venv\\Scripts\\activate")
        print("  python manage.py runserver")
    else:
        print("  source venv/bin/activate")
        print("  python manage.py runserver")
    print()
    print("Then open: http://127.0.0.1:8000")
    print()
    print("Admin panel: http://127.0.0.1:8000/admin/")
    print()
    print("Email notifications go to: d3khan2.0@gmail.com")
    print("(Currently printing to console in development mode)")
    print()
    print("To send REAL emails, edit d3khan_blog/settings.py")
    print("and configure the SMTP section.")
    print()
    print("Happy blogging!")

if __name__ == "__main__":
    main()
