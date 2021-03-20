from django.contrib import admin
from blog.models import Post, Comment

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'body', 'publish', 'created', 'updated',  'status' ]
    list_filter = ('status','author', 'created', 'title')
    search_fields = ('body', 'title')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    prepopulated_fields = {'slug': ('title',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'body')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('body', 'name', 'email')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
