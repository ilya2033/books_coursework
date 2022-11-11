from django.shortcuts import  reverse,redirect
from django.http import  HttpResponseRedirect,  JsonResponse

from django.template.context_processors import csrf
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm
from django.contrib.auth.forms import UserCreationForm 
import json





#Обработка входа пользователля в аккаунт 
def login(request):
	context = {}
	login_form = LoginForm(request.POST)
	if login_form.is_valid():
		username = login_form.cleaned_data.get('username')
		password = login_form.cleaned_data.get('password')
		user = auth.authenticate(username = username, password = password)
		if user is not None:
			if not login_form.cleaned_data.get('remeber_me'):
				request.session.set_expiry(0)
			auth.login(request,user)
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		else:
			messages.error(request,'Неверный логин или пароль')
	else:
		messages.error(request,login_form.errors['__all__'].as_text())

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



#Обработка выхода пользователя из аккаунта 
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



#Обработка регисрации пользователя 
def register(request):
	args = {}
	context = {}
	if request.POST:
		newuser_form = RegisterForm(request.POST)
		if newuser_form.is_valid():
			if User.objects.filter(username = newuser_form.cleaned_data['username'] ).exists():
				
				context.update({'username':'Пользователь с таким именем уже существует'})
				json.dumps(context)
				return JsonResponse(context)
			else:
				newuser_form.save()
				newuser = auth.authenticate(username = newuser_form.cleaned_data['username'],password = newuser_form.cleaned_data['password2'])
				auth.login(request,newuser)
				return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		else:
			if request.is_ajax():

				for field in newuser_form.errors:
					context.update({str(field):str(newuser_form.errors[field].as_text())})
				json.dumps(context)
				return JsonResponse(context)
	return 0




#Проверка авторизации пользвателя 
def check_login(request,username):
	context = {}
	if  request.is_ajax():
		if username == request.user.username:
				context.update({'result':False})
		else:
			context.update({'result':User.objects.filter(username=username).exists()})
		json.dumps(context)
		return JsonResponse(context)






#Проверка формы регистрации 
def check_register(request):
	args = {}
	context = {}
	args['form'] = RegisterForm()
	if request.POST and request.is_ajax():
		newuser_form = RegisterForm(request.POST)
		if newuser_form.is_valid():
			if User.objects.filter(username = newuser_form.cleaned_data['username'] ).exists():
				context.update({'result':False})
				context.update({'username':'Пользователь с таким именем уже существует'})
				json.dumps(context)
				return JsonResponse(context)
			else:
				context.update({'result':True})
				json.dumps(context)
				return JsonResponse(context)
		else:
			context.update({'result':False})
			for field in newuser_form.errors:
				context.update({str(field):str(newuser_form.errors[field].as_text())})
			json.dumps(context)
			return JsonResponse(context)
	return 0