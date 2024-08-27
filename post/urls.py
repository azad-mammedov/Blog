from django.urls import path
from .views import PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('new/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>', PostUpdateView.as_view(), name='post_detail'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]