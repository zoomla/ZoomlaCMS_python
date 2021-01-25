from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager


# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset() \
            .filter(status='published')


# 发帖、邮件传送等模型
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    # body = models.TextField()
    body = RichTextUploadingField(default='', verbose_name='内容详情')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)  # 采用auto_now_add当创建某个对象时，日期自动保存
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()  # 引入tag标签

    # 模型的标准url
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


# 评论系统
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on{}'.format(self.name, self.post)
