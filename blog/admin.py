from django.contrib import admin
from django.contrib.admin.decorators import display
from blog.models import BlogPost, Comment, BlogCategory


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list = ('title')
    search_fields = [('title')]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content','created_at', 'blog','updated_at')
    list_filter = ('user', 'content','created_at', 'blog','updated_at')
    search_fields = ('user', 'content','created_at', 'blog','updated_at')

admin.site.register(Comment, CommentAdmin)


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ( 'title','content','created_at', 'image', 'author')
    list_filter = ( 'title','content','created_at', 'image', 'author')
    search_fields = ('title','content','created_at', 'image', 'author')


admin.site.register(BlogPost, BlogPostAdmin)







