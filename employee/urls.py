"""employee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path

from user import views

urlpatterns = [
    #    path("admin/", admin.site.urls),
    # 部门管理
    path('depart/list/', views.depart_list),
    path('depart/add/', views.depart_add),
    path('depart/delete/<int:nid>', views.depart_delete, name='depart_delete'),
    path('depart/edit/<int:nid>', views.depart_edit, name='depart_edit'),

    #
    path('user/list/', views.user_list),
    path('user/add/', views.user_add),

    path('user/model/add/', views.user_model_add),
    path('user/edit/<int:nid>', views.user_edit, name='user_edit'),
    path('user/delete/<int:nid>', views.user_delete, name='user_delete'),

    path('pretty/list/', views.pretty_list),
    path('pretty/add/', views.pretty_add),
    path('pretty/edit/<int:nid>', views.pretty_edit, name='pretty_edit'),
    path('pretty/delete/<int:nid>', views.pretty_delete, name='pretty_delete'),
]
