from django import forms
from .models import User, App_Password, OTP_codes
from django.forms import ValidationError

class SignUp_Form(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(),
        }

        def clean(self):
            cleaned_data = super().clean()

            username = cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                raise ValidationError('Ushbu username band!')

            email = cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                raise ValidationError('Ushbu email band!')

            password = cleaned_data.get('password')
            confirm_password = cleaned_data.get('confirm_password')

            if password != confirm_password:
                raise ValidationError('Parollar mos emas!')


            return cleaned_data

class App_Password_Form(forms.ModelForm):

    class Meta:
        model = App_Password
        fields = [
            'website_name', 'link', 'app_password'
        ]           

class OTP_Code_Form(forms.ModelForm):
    class Meta:
        model = OTP_codes
        fields =['code']
