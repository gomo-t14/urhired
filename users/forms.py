from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset,  HTML , Column , Field , Row , Div
from crispy_tailwind.layout import Submit
from crispy_tailwind.tailwind import CSSContainer 


#instantiate the user model
User = get_user_model()

#define your forms here
#form for registering user
class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User 
        fields = ('email', 'nationality')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2  and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit = True):
        user = super().save(commit=False) #creates user without saving to database
        user.set_password(self.cleaned_data['password1']) #hashes user password
        user.is_active = True
        if commit:
            user.save() #saves user to db 
        return user


    #here we specify the helper to  customise the form
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout (
            Div(
            Fieldset('Register' ,
            Field('email' , placeholder = 'Email Address', css_class='input '),
            Field('nationality',placeholder = 'Nationality', css_class='input '),
            Field('password1',placeholder = '********', css_class='input '),
            Field('password2',placeholder = '********', css_class='input'),
            Submit('submit', 'Register', css_class='btn btn-soft btn-primary'),
            css_class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4 shadow-md text-4xl"
            ),
            css_class= "mx-auto"
        ) ,
      
        )

#form for creating super user
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'nationality')

#form for logging in 
class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))

    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout (
            Div(
            Fieldset('Log In' ,
            Field('username' , placeholder = 'Email Address', css_class='input '),
            Field('password',placeholder = '********', css_class='input '),
            Submit('submit', 'Register', css_class='btn btn-soft btn-primary'),
            css_class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4 shadow-md text-4xl"
            ),
            css_class= "mx-auto"
        ) ,
      
        )


#form to update email or nationality
class UserUpdateForm(CustomUserCreationForm):
    pass