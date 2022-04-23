from django.contrib import admin
from django.urls import path

from api import views
from blog.yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.PostsView.as_view()),
    path('posts/<int:pk>/', views.PostsDetailView.as_view()),
    path('posts/<int:pk>/comments', views.CommentsView.as_view()),
    path('posts/<int:pk>/comment/<int:cid>', views.CommentDetailView.as_view()),
    path('posts/<int:pk>/comment/<int:cid>/replies', views.RepliesView.as_view()),
]

urlpatterns += doc_urls
