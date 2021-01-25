from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger
# 使用基于类的视图，并使用Django提供的通用listview,这一基视图可显示任意类型的对象：
from django.views.generic import ListView
# 引入搜索表单
from django.contrib.postgres.search import SearchVector

# 邮件表单 评论表单
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count


# Create your views here.

# 显示帖子列表
def post_list(request):
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})


# 显示独立帖子
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # 当前帖子的评论列表以及发表等
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # 已表评论
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    # 相似性检索帖子
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]  # 检索前四个

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # 三个一页
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页面不是完整的，则生成第一页
        posts = paginator.page(1)
    except EmptyPage:
        # 如果页面超出范围，则传递结果的最后一页
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts,
                   'tag': tag})


def post_share(request, post_id):
    # 检索帖子ID
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == "POST":
        # 表单发送
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # 表单字段通过验证
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{}({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@z01.com', [cd['to']])
            sent = True
            # 发送邮件
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


# 构建搜索视图
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.annotate(search=SearchVector('title', 'body'), ).filter(search=query)
    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})
