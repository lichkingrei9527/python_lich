from django.urls import path

from . import views

urlpatterns = [
    # path (
    # route 字符串，表示 URL 规则，与之匹配的 URL 会执行对应的第二个参数 view
    # view 用于执行与正则表达式匹配的 URL 请求
    # kwargs 视图使用的字典类型的参数
    # name 用来反向获取 URL
    # ) 四个参数
    path('', views.index, name='index'),
]
