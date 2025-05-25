from django.urls import path
from . import views
from .views import CustomLoginView,  RegisterView,EditProfileView , ProfileView , DeleteAccountView ,CustomPasswordResetView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('home/', views.home_view,name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page = 'login'), name='logout'),
    path('', RegisterView.as_view(), name='register'),
    path('edit_profile/',views.EditProfileView, name = 'editProfile'), # path to edit profile
    path('profile/',ProfileView , name = 'profile'),#path to view profile
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),  
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),   
    path('delete-account/', DeleteAccountView.as_view(), name='delete_account'),
]
