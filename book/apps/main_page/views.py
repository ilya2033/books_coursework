from django.shortcuts import render
from django.template.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm 
from loginsys.forms import LoginForm


from items.models import Item




#Обработка главной страници 
def index(request):
	context = {}
	context.update(csrf(request))
	items = Item.objects.order_by('-last_upd')[:20]
	context = {
		'items':items,
		'username': auth.get_user(request).username,
		'register_form': UserCreationForm(),
		'login_form': LoginForm(),
	}	
	return render(request,"index.html",context) 
