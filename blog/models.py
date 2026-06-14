
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
