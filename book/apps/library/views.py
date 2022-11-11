from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages

import json
import operator 


from .models import Library,item_status
from items.models import Item 




def ajax_add_status(request, item_id):
	context = {}
	if request.user.is_authenticated and request.is_ajax():
		POST_status = request.POST.get('status').upper()
		if item_status.STATUS[str(POST_status)]:
			POST_status =  operator.attrgetter("STATUS."+ str(POST_status))(item_status)
			user = User(request.user.id)
			try:
				user.library
			except:
				Library.objects.create(user=user)

			try: 
				user.library.items.get(id = item_id)
			except:
				user.library.items.add(item_id)

			try:
				user.library.items.get(id = item_id)
			except:
				user.library.items.add(Item.objects.get(id = item_id))


			try:
				status =user.library.items.get(id = item_id).user_status.get(user = request.user)
			except:
				status = user.library.items.get(id = item_id).user_status.create(user = request.user, item = item_id)

			status.status = POST_status
			status.save()
			context.update({'status':status.status, 'result':'success'})
			json.dumps(context)
			return JsonResponse(context)	
	else:
		if not  request.user.is_authenticated:
			messages.error(request,'Войдите или зрегистрируйтесь')
		json.dumps(context)
		return JsonResponse(context)	





def ajax_get_libliary(request, status):
	context = {}
	status = status.upper()
	if request.user.is_authenticated and request.is_ajax():
		user = User(request.user.id)
		try:
			user.library
		except:
			Library.objects.create(user=user)

		if status == 'ALL':
			items = user.library.items.filter(user_status__user = request.user).order_by('-item_date')
		else:
			status =  operator.attrgetter("STATUS."+ str(status))(item_status)
			items = user.library.items.filter(user_status__user = request.user).filter(user_status__status = status).order_by('-item_date')

	
		if items.count()>0:
			context['result'] = True
			for title in items:
				context.update({title.id:{
						'Title':title.item_title,
						'Item_image':title.get_image_url(),
						'item_desc':title.item_desc[:300]
					}})
		json.dumps(context)
		return JsonResponse(context)	
	else:
		if not  request.user.is_authenticated:
			messages.error(request,'Войдите или зрегистрируйтесь')
		json.dumps(context)
		return JsonResponse(context)	