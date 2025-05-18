from django.urls import path
from . import views
from .views import CustomLoginView, CustomLogoutView, RegisterView, EditProfileView , ProfileView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('home/', views.home_view,name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('edit_profile/',EditProfileView, name = 'editProfile'), # path to edit profile
    path('profile/',ProfileView , name = 'profile'),#path to view profile
    
]
