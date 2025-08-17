"""
URL configuration for blog_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from base.views import CategoryApiView,TagApiView, PostApiView, CommentApiView, UserApiView

urlpatterns = [
    path('admin/', admin.site.urls),

    #Catagories 
    path ('Categories/', CategoryApiView.as_view({'get': 'list', 'post': 'create'})),
    path('Categories/<int:pk>/', CategoryApiView.as_view({'get':'retrieve','put':'update','delete':'destroy'})),
    
    #Tag 
    path('tags/', TagApiView.as_view({'get': 'list', 'post': 'create'})),
    path('tags/<int:pk>/', TagApiView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # Post 
    path('posts/', PostApiView.as_view({'get': 'list', 'post': 'create'})),
    path('posts/<int:pk>/', PostApiView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('posts/<int:pk>/publish/', PostApiView.as_view({'patch': 'publish'})),  # custom action

    # Comment 
    path('comments/', CommentApiView.as_view({'get': 'list', 'post': 'create'})),
    path('comments/<int:pk>/', CommentApiView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('posts/<int:post_id>/comments/', CommentApiView.as_view({'get': 'list_by_post'})),

    # User 
    path("user/",UserApiView.as_view({'get':'list','post':'create'})),
    path('register/', UserApiView.as_view({'post': 'register'})),
    path('login/', UserApiView.as_view({'post': 'login'})),
]