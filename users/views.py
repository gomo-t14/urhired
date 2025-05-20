from django.shortcuts import render , redirect
from django.contrib.auth.views import LoginView, LogoutView 
from django.views.generic.edit import CreateView 
from django.urls import reverse_lazy
from django.http import HttpResponse
from .forms import RegisterForm , CustomLoginForm , UserCreationForm
from django.contrib.auth.decorators import login_required


# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = CustomLoginForm
    success_url = reverse_lazy('home')
    

class CustomLogoutView(LogoutView):
    template_name = 'users/home.html'

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')


#redirects to home page
def home_view(request):
    return render(request, 'users/home.html')



#edits user 
@login_required
def EditProfileView(request):

    user = request.user #get currently logged in user

    if request.method == 'POST':
        form = UserCreationForm(request.POST, instance = user)

        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            form = UserCreationForm(isinstance = user)

        return render(request, 'users/edit_profile.html', {'form':form})
    
# profile view 
@login_required
def ProfileView(request):
    return render(request, 'users/profile.html', {'user':request.user})





    