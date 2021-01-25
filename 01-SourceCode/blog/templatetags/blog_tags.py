from django import template
from ..models import Post

register = template.Library()


# 博客列表的总数统计
@register.simple_tag
def total_posts():
    return Post.published.count()


# 博客列表页显示最近更新
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):  # 最近五篇
    last_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': last_posts}

# 文章详情页-随便看看显示最近更新
@register.inclusion_tag('blog/post/latest_random.html')
def show_latest_random(count=5):  # 最近五篇
    last_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': last_posts}


# 生成简单的模板标徐清，并在变量中存储当前结果，以供后续操作复用，而非直接对其予以输出
from django.db.models import Count


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]


# 支持Markdown语法
from django.utils.safestring import mark_safe
import markdown


@register.filter(name='markdown')
def markdown_fromat(text):
    return mark_safe(markdown.markdown(text))
