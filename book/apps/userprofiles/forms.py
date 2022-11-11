from django import forms
from .models import Profile
from django.contrib.auth.models import User
import re


#Форма профиля 
class ProfileForm(forms.ModelForm):
	username = forms.CharField()

	def __init__(self, username ,*args, **kwargs):
	    self.cur_username = username
	    super().__init__(*args, **kwargs)


	class Meta:
		model = Profile
		fields = ('first_name','last_name','image','bio','location')

		widgets = {
			'bio': forms.Textarea(attrs=
				{'name':'text','class':'form-control w-100',
				'placeholder':'bio', 'rows': 4, 'cols': 100,}),
		}

	#Валидация username
	def clean_username(self):
	    data = self.cleaned_data
	    regex = r'^[\w.@+-]+$'
	    username = data.get("username")


	    if User.objects.filter(username= username).exists() and username != self.cur_username:
	        raise forms.ValidationError('username уже занят')

	    if not re.match(regex,data.get('username')):
	    	raise forms.ValidationError('Не более 150 символов. Только буквы, цифры и символы @.+-_ ')



	    return username
