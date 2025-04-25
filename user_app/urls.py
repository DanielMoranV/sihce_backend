from django.urls import path
from user_app.views import UserListCreateView, UserDetailView

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
