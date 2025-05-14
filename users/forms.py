from django import forms
from django.contrib.auth import get_user_model

#instantiate the user model
User = get_user_model()

#define your forms here
class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User 
        fields = ('email', 'nationality')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password1')
        if password1 and password2  and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit = True):
        user = super().save(commit=False) #creates user without saving to database
        user.set_password(self.cleaned_data['password1']) #hashes user password
        if commit:
            user.save() #saves user to db 
        return user