
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'created_at', 'is_placeholder']
    list_filter = ['category', 'is_placeholder', 'created_at']
    search_fields = ['title', 'content', 'author']
    date_hierarchy = 'created_at'
