from django.urls import path
from .views import (
    PostCreateView, 
    PostDetailView, 
    PostDeleteView
    )

urlpatterns = [
    path('new/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]