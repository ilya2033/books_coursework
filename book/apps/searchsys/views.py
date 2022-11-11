from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q

from django.template.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm 
from loginsys.forms import LoginForm




import json


from items.utils import order_by, norm_orders, get_dict_key
from items.models import Item





#Обработка поиска книги без перезагрузки страници 
def ajax_search_item(request,data):

	context = {}
	context.update({'result':False})
	if request.is_ajax() and data != '' and data != None:
		titles = Item.objects.filter(Q(item_title__contains = data) | Q(item_other_title__contains = data) )[:5]
		if titles.count()>0:
			context['result'] = True
			for title in titles:
				context.update({title.id:{
						'Title':title.item_title,
						'Item_image':title.get_image_url(),
						'item_desc':title.item_desc[:200]
					}})
	json.dumps(context)
	return JsonResponse(context)






#Обработка поиска книги с перезагрузкой страници 
def search_item(request):
	context = {}
	context.update(csrf(request))
	if request.POST and request.POST['text'] != '' and request.POST['text'] != None:
		item_list = Item.objects.filter(Q(item_title__contains = request.POST['text']) | Q(item_other_title__contains = request.POST['text'])  )

		context = {
			'items':item_list,
			'username': auth.get_user(request).username,
			'tag_list': Item.tags.all(),
			'register_form': UserCreationForm(),
			'login_form': LoginForm(),
			'orders':order_by ,
			'norm_orders':norm_orders,			
		}		
	return render(request,"items.html",context) 




#обработка поиска по тегу 
def tag(request,tag):	
	context = {}
	context.update(csrf(request))
	item_list = Item.objects.filter(tags__slug = tag)

	context = {
		'items':item_list,
		'username': auth.get_user(request).username,
		'username': auth.get_user(request).username,
		'register_form': UserCreationForm(),
		'login_form': LoginForm(),
		'tag_list': Item.tags.all().exclude(slug = tag),
		'pos_tags':[Item.tags.get(slug = tag ),],
		'orders':order_by ,
		'norm_orders':norm_orders,
	}	

	return render(request,"items.html",context)

















#обработка поиска по тегу + сортировки без перезагрузки сраници 
def ajax_tag(request,pos_tags,neg_tags,order):	
	context = {}
	context['result'] = False
	if request.is_ajax():
		pos_tags_list = ''	
		neg_tags_list = ''	
		item_list = Item.objects.all() 
		if pos_tags != '': 
			for tag in pos_tags.split('+'):
				tag = tag.replace('"','').replace(']','').replace('[','')
				item_list = item_list.filter(tags__slug = tag )
				if pos_tags_list:
					instance = Item.tags.get(slug = tag)
					pos_tags_list |= Item.tags.filter(pk=instance.pk)
				else:
					pos_tags_list = Item.tags.filter(slug=tag)
				

		if neg_tags != '': 
			for tag in neg_tags.split('+'):
				tag = tag.replace('"','').replace(']','').replace('[','')
				item_list = item_list.exclude(tags__slug = tag )
				if neg_tags_list:
					instance = Item.tags.get(slug = tag)
					neg_tags_list |= Item.tags.filter(pk=instance.pk)
				else:
					neg_tags_list = Item.tags.filter(slug=tag)



		if item_list.order_by(str(order)).count()>0:
			context['result'] = True
			i = 0
			for title in item_list.order_by(order):

				context.update({i:{
						'id':title.id,
						'Title':title.item_title,
						'Item_image':title.get_image_url(),
					}})
				i=i+1

	json.dumps(context)
	return JsonResponse(context)





#Поиск тегов 
def ajax_search_tag(request,exclude_tags,data):

	context = {}
	context.update({'result':False})
	if request.is_ajax() and data != '' and data != None:
		tags = Item.tags.filter(Q(name__contains = data) | Q(slug__contains = data) )


		if exclude_tags != '': 
			for tag in exclude_tags.split('+'):
				tag = tag.replace('"','').replace(']','').replace('[','')
				tags = tags.exclude(slug = tag )


		if tags.count()>0:
			context['result'] = True
			for tag in tags:
				context.update({tag.id:{
						'Name':tag.name,
						'Slug':tag.slug,
					}})
	json.dumps(context)
	return JsonResponse(context)