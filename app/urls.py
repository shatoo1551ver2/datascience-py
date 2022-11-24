from importlib.abc import PathEntryFinder
from django.urls import path
from . import views    

app_name = 'app'

urlpatterns = [
    path('', views.starter, name='starter'),
    path('index/', views.index, name='index'),
    path('index2/', views.index2, name='index2'),
    path('detail/', views.detail, name='detail'),  # 追記
    path('import/', views.PostImport.as_view(), name='import'),
    path('export/', views.PostExport, name='export'),
    path('list/', views.List.as_view(), name='list'), #"追加")
    path('data/', views.data, name='data'), #"追加")


    # path('', Create.as_view(), name='home'),
    # path('list/', listfunc, name='list'),
    # path('article/<int:article_id>/', wordlistfunc, name='wordlist'),
    # path('home_api',apihomeview, name='home_api'),
    # path('apiregiview',apiregiview, name='apiregiview'),
    # path('api_regi',apiregi, name='api_regi'),
    # path('api_room/<int:api_id>/',apiroom, name='api_room'),
    # path('apidatacreate/<int:api_id>/',apidatacreate, name='apidatacreate'),
    # path('api_delete/<int:api_id>/', api_delete, name='api_delete'),
]
