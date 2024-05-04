from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='homepage'),
    path('search', views.search_form, name='search'),
    path('user/<str:username>/', views.user_profile_view, name='user-profile'),
    path('user/list', views.UserListView.as_view(), name='user-list'),
]
