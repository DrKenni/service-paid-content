from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserUpdateView, RegisterView, UserDetailView, UserView, SubPlanCreateView, SubPlanListView

app_name = UsersConfig.name

urlpatterns = [
    # Authenticate
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    # User prof
    path('profile/<int:pk>/', UserDetailView.as_view(), name='profile'),
    path('profile/edit/', UserUpdateView.as_view(), name='user_edit'),
    path('profile/plan/create/', SubPlanCreateView.as_view(), name='plan_create'),
    # Users
    path('user/list/', UserView.as_view(), name='user_list'),
    # Plan
    path('profile/plan/list/<int:pk>', SubPlanListView.as_view(), name='plan_list'),
]
