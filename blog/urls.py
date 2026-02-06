from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<uuid:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
    
    # API Endpoints
    path('api/posts/', views.api_get_blogs, name='api_get_blogs'),
    path('api/posts/<uuid:post_id>/', views.api_get_post_detail, name='api_get_post_detail'),
    path('api/posts/create/', views.api_create_post, name='api_create_post'),
    
    # Documentation
    path('docs/', views.api_docs_view, name='api_docs'),
    
    path('post/<uuid:post_id>/delete/', views.delete_post, name='delete_post'),
]
