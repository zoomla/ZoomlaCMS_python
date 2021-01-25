from django.urls import path  # 导入path
from . import views

urlpatterns = [
    # path('', views.article_list),
    path('我爱逐浪', views.get_fage_datetime),
    path('', views.well_index),
]
