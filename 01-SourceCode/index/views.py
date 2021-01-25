from django.db.models import Index
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime


# Create your views here.


# Create your views here.


# from index.models import Index, User

#
# def article_list(request):
#     articles = Article.objects.all()  # 从article表中获取数据
#     return render(request, 'index.html', {"articles": articles})  # 渲染模板


def year_archive(request, year):
    return HttpResponse(f'year_archive函数接收参数year:{year}')


def month_archive(request, year, month):
    return HttpResponse(f'month_archive函数接收参数Year{year}, month:{month}')


def article_detail(request, year, month, slug):
    return HttpResponse(f'article_detail函数接收参数year:{year},month:{month},slug:{slug}')


def get_current_datetime(request):  # 定义一个视图方法，必须带有请求对象作为参数
    today = datetime.today()  # 请求的时间
    format_today = today.strftime('%Y-%m-%d')
    html = f"<html><body>今天是：{format_today}</body></html>"  # 生成html代码
    return HttpResponse(html)  # 将响应发送给客户端输出


def get_fage_datetime(request):  # 定义一个视图方法，必须带有请求对象作为参数
    today = datetime.today()  # 请求的时间
    format_today = today.strftime('%Y-%m-%d')
    html = f"<html><body>今天是：{format_today}</body></html>"  # 生成html代码
    return HttpResponse(html)  # 将响应发送给客户端输出

def get_zoomla_well(request):  # 定义一个视图方法，必须带有请求对象作为参数
    today = datetime.today()  # 请求的时间
    format_today = today.strftime('%Y-%m-%d')
    html = f"<html><body>Zoomla!逐浪CMS python版 <br/> 今天是：{format_today}</body></html>"  # 生成html代码
    return HttpResponse(html)  # 将响应发送给客户端输出


# 绑定一个模板
def well_index(request):
    return render(request, 'index.html')
