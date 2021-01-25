from django.contrib import admin
from .models import Post, Comment


# Register your models here.
# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):  # blog项目（Post)后台列表显示与筛选的自定义
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


# 后台绑定评论
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

# 绑定Post模型到PostAdmin管理后台
# admin.site.register(Post, PostAdmin)
