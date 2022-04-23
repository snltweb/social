from django.urls import path
from django.contrib.auth import views as auth_views
from .views import PostListView,PostDetailView

urlpatterns = [
    path('', PostListView.as_view(),name='post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    
]
