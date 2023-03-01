from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser

class UserRegistrForm(UserCreationForm):
    username = forms.CharField(min_length=4,
                               max_length=20,
                               label='Логин',
                               widget=forms.TextInput(attrs={'class':'form-control'}),
                               help_text="Максимум 20 символов. Может содержать только буквы, цифры и знаки @ / . / + / - / _")
    email = forms.EmailField(label='E-mail',
                             widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(max_length=25,
                                label="Пароль",
                                widget=forms.PasswordInput(attrs={'class':'form-control'}),
                                help_text="Пароль должен состоять от 8 до 25 символов")
    password2 = forms.CharField(max_length=25,
                                label="Подтвердите пароль",
                                widget=forms.PasswordInput(attrs={'class':'form-control'}),
                                help_text="Повторите пароль")


    class Meta:
        model = CustomUser
        fields=('username',
                'email',
                'password1',
                'password2')
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control'})
        }

class LoginUser(AuthenticationForm):
    username = forms.CharField(min_length=4,
                               max_length=20,
                               label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-control'}),
                               help_text="Введите ваш логин")
    password = forms.CharField(max_length=25,
                                label="Пароль",
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username',)

class AcceptJurnalistFrom(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields =('username','is_journalist')
        
class UserData(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','email')