from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.views import LoginView , PasswordResetView 
from django.views.generic.edit import CreateView , DeleteView 
from django.urls import reverse_lazy
from django.http import HttpResponse
from .forms import RegisterForm , CustomLoginForm , UserCreationForm ,CustomPasswordResetForm ,ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .models import Profile



# Create your views here.
User = get_user_model() #gets instance of currently logged in user 

#view to reset password
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

#Delete the currently logged in account
class DeleteAccountView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/delete_account.html'
    success_url = reverse_lazy('register')  
    def get_object(self):
        return self.request.user
    
class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = CustomLoginForm
    success_url = reverse_lazy('home')
    

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')


#redirects to home page
@login_required
def home_view(request):
    return render(request, 'users/home.html')



#edits user 
@login_required
def EditProfileView(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # change to your profile view name
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form})
    
# profile view 
@login_required
def ProfileView(request):
    return render(request, 'users/profile.html', {'user':request.user})








    