from django import forms
from django.contrib.auth.forms import UserCreationForm 
import re

#Форма регистарции 
class RegisterForm(UserCreationForm):
	def serialize(self):
		return {
		   'username' : self.cleaned_data['username'],
		   'password1': self.cleaned_data['password1'],
		}


class LoginForm(forms.Form):
	username = forms.CharField(label = 'Логин',max_length=150)
	password = forms.CharField(label = 'Пароль',widget=forms.PasswordInput)
	remeber_me = forms.BooleanField(label='Запомнить',required = False)

	def clean(self):
		data = self.cleaned_data
		regex = r'^[\w.@+-]+$'
		username = data.get("username")
		password = data.get("password")


		if not re.match(regex,data.get('username')) or not re.match(regex,data.get('password')):
			raise forms.ValidationError('Только буквы, цифры и символы @.+-_')


		return data

