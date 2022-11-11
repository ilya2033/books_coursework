from django.shortcuts import render, reverse,redirect
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm 
from .models import Profile
from .forms import ProfileForm
from PIL import Image

import re
from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator


from library.models import item_status, Library
from loginsys.forms import LoginForm




#Обработка своей страници профиля 
def index(request):
	if request.user.username:
		pass
	else:
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	try:
		profile=request.user.profile
	except:
		profile = Profile()
		profile.user = request.user
		if profile:
			profile.save()
	try:
		request.user.library
	except:
		Library.objects.create(user=request.user)
	context = {}
	context.update(csrf(request))

	items = request.user.library.items.filter(user_status__user = request.user).order_by('-item_date')
	if items.count() > 1:
		items_many = True
	else :
		items_many = False
	context = {
		'profile':profile,
		'form':ProfileForm( request.user.username,
							initial={'first_name': profile.first_name,
									'last_name': profile.last_name,
									'username':request.user.username,
									'bio': profile.bio,
									'location':profile.location}),
		'register_form': UserCreationForm(),
		'login_form': LoginForm(),
		'items':items,
		'status':item_status,
		'items_many':items_many,
	}
	return render(request,"userprofile.html",context)



#Обработка чужой страници профиля 
def show_profile(request,profile_id):
	context = {}
	context.update(csrf(request))
	if not request.user.is_anonymous:
		if auth.get_user(request).profile.id == profile_id:
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	profile = Profile.objects.get(id=profile_id)
	context = {
		'profile':profile,
	}
	return render(request,'profileview.html',context)




#Обработка обновления профиля 
def update_profile(request):
	context = {}
	context.update(csrf(request))
	profile = Profile.objects.get(id =request.user.profile.id)
	if request.POST:
		profile_form = ProfileForm(request.user.username,request.POST, request.FILES,)
		if profile_form.is_valid():
			profile.user_id = request.user.id
			profile.first_name = profile_form.cleaned_data['first_name']
			profile.last_name = profile_form.cleaned_data['last_name']
			profile.location = profile_form.cleaned_data['location']
			profile.bio = profile_form.cleaned_data['bio']
			request.user.username = profile_form.cleaned_data['username']
			request.user.save()

			if profile.image and profile_form.cleaned_data['image'] != None :
				profile.save_image()
				image_root = settings.PROJECT_ROOT+profile.image_url
				profile.image = profile_form.cleaned_data['image']
			elif not profile.image and profile_form.cleaned_data['image'] != None:
				profile.image = prqofile_form.cleaned_data['image']
				image_root = settings.PROJECT_ROOT+profile.image_url

			profile.save()

			messages.info(request,'Пофиль был обновлен')

			if profile.image: 
				crop_image(settings.PROJECT_ROOT+profile.image_url,settings.PROJECT_ROOT+profile.image_url,)
				scale_image(settings.PROJECT_ROOT+profile.image_url,settings.PROJECT_ROOT+profile.image_url,200,200)



		items = request.user.library.items.filter(user_status__user = request.user).order_by('-item_date')
		if items.count() > 1:
			items_many = True
		else :
			items_many = False
	context = {
		'profile':profile,
		'form':profile_form,
		'register_form': UserCreationForm(),
		'login_form': LoginForm(),
		'items':items,
		'status':item_status,
		'items_many':items_many,
	}
	return render(request,'userprofile.html',context)




#Масштабирование изображения 
def scale_image(input_image_path,output_image_path,width=None,height=None):
	original_image = Image.open(input_image_path)
	w, h = original_image.size

	if width and height:
		max_size = (width, height)
	elif width:
		max_size = (width, h)
	elif height:
		max_size = (w, height)
	else:
		raise RuntimeError('Width or height required!')

	original_image.thumbnail(max_size, Image.ANTIALIAS)
	original_image.save(output_image_path)

	scaled_image = Image.open(output_image_path)
	width, height = scaled_image.size



#обрезка изображения 
def crop_image(input_image_path,output_image_path,):
	img = Image.open(input_image_path)
	width, height = img.size
	if width>height:
		size = width - height
		area = (size/2,0,size/2+height,height)
	elif height>width:
		size = height - width
		area = (0,size/2,width,size/2+width)
	else:
		return 0

	cropped_img = img.crop(area)
	cropped_img.save(output_image_path)
