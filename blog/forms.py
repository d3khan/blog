
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
