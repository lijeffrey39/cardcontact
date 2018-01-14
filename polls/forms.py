from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserChangeForm


class UserForm(forms.ModelForm):
	password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Choose a Password'}))
	email = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control','placeholder': 'Email'}))
	username = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control','placeholder': 'Username'}))
	first_name = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control','placeholder': 'First Name'}))
	last_name = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control','placeholder': 'Last Name'}))

	class Meta:
		model = User
		fields = ['email', 'username', 'first_name', 'last_name', 'password']


class UserFormLogin(forms.Form):
	username = forms.CharField(widget = forms.TextInput(
		attrs={
		'class': 'form-control',
		'placeholder': 'Username'
		}
		))
	password = forms.CharField(widget = forms.PasswordInput(
		attrs={
		'class': 'form-control',
		'placeholder': 'Password'
		}
		))

	def clean(self, *args, **kwargs):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		user = authenticate(username = username, password = password)
		if username and password:
			if not user:
				raise forms.ValidationError("Not a User")

			if not user.check_password(password):
				raise forms.ValidationError("Incorrect Password")

			if not user.is_active:
				raise forms.ValidationError("Bad User")

			return super(UserFormLogin, self).clean(*args, **kwargs)


class EditProfileForm(UserChangeForm):

	class Meta:
		model = User
		fields = (
			'email',
			'first_name',
			'last_name',
			'password')
		widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EditProfileFormRest(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('phone', 'facebook','snapchat', 'insta', 'twitter')
		widgets = {
			'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control'}),
            'snapchat': forms.TextInput(attrs={'class': 'form-control'}),
            'insta': forms.TextInput(attrs={'class': 'form-control'}),
            'twitter': forms.TextInput(attrs={'class': 'form-control'}),
        }