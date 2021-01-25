"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
# from editer import views
from blog import views
from index import views
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap

# 引用sitemap

sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('index.urls')),
                  path('blog/', include('blog.urls', namespace='blog')),
                  path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
                  path('account/', include('account.urls')),  # 导入account用户系统
                  url(r'^ckeditor/', include('ckeditor_uploader.urls')),
                  # url(r'^blog/', views.blog),  # 测试获取后台编辑的内容用的
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 没有这一句无法显示上传的图片
