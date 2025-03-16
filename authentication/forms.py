from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

#SignupForm

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, error_messages={'required': 'Username is required.'})
    email = forms.EmailField(required=True, error_messages={'required': 'Email is required.', 'invalid': 'Please enter a valid email address.'})
    password = forms.CharField(widget=forms.PasswordInput, required=True, validators=[
        RegexValidator(
            regex='^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$',
            message='Password must contain at least 8 characters, including at least one uppercase letter, one lowercase letter, one digit, and one special character.'
        )
    ])
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True, error_messages={'required': 'Confirm password is required.'})

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')

        return cleaned_data


#Login form 
# class LoginForm(forms.Form):
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'Email'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Password'}))
    
from django import forms
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Password'}))
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        
        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError('Invalid email or password.')
        return cleaned_data




# Add the following line to set the label style
    email.label = 'Email'
    email.label_class = 'times-new-roman bold'


#For user profile in nav-bar
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']




