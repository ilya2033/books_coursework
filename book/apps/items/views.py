from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.template.context_processors import csrf
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
import json



from .models import Item, Comment,Like
from .forms import CommentForm
from .utils import order_by,norm_orders
from library.models import Library, item_status, Rating
from userprofiles.models import Profile
from loginsys.forms import LoginForm


#Оброботка страницы каталога 
def index(request):
	context = {}
	context.update(csrf(request))
	context = {
		'items':Item.objects.all().order_by('item_date'),
		'username': auth.get_user(request).username,
		'register_form': UserCreationForm(),
		'login_form': LoginForm(),
		'tag_list': Item.tags.all(),
		'orders':order_by,
		'norm_orders':norm_orders,

	}	

	return render(request,"items.html",context) 



#Обработка страницы книги 
def item(request, item_id):
	context = {}
	context.update(csrf(request))
	item = Item.objects.get(id = item_id)
	lib_item = ''
	pages = {}

	if item.comments.count() > 20:
		context['max_comments'] = True
	else:
		context['max_comments'] = False


	if request.user.is_authenticated:

		try:
			lib_item =request.user.library.items.get(id = item.id).user_status.get(user = request.user)
		except:
			pass

			
	comments_list = item.comments.filter(parent__isnull = True).order_by('-comment_date')[:20]





	context.update({
		'item':item,
		'last_upd':Item.objects.order_by('-last_upd')[:3],
		'comments':comments_list,
		'username': auth.get_user(request).username,
		'comment_form':CommentForm(),
		'tags': item.tags.all(),
		'lib_item':lib_item,
		'status': item_status,
		'rating':Rating.item_rating(item.id),
		'score_range' :range(1,Rating.max_score+1) ,
		"max_score" :Rating.max_score,
		'register_form': UserCreationForm(),
		'login_form': LoginForm(),
	})



	return render(request,"item.html",context)





#Обработка рейтинга книги 
def item_rating(request,item_id):
	item = Item.objects.get(id= item_id)
	context = {}
	context.update({'result':False})
	if request.user.is_authenticated and request.is_ajax() and request.POST:
		score = int(request.POST.get('score'))
		if score >0 and  score <= Rating.max_score :
			try:
				item.user_rating.get(user = request.user)
			except:
				Rating.objects.create(item=item,user = request.user,score = score)

			rating = item.user_rating.get(user = request.user)
			rating.score = int(score)
			rating.save()

			context.update({
				"score":rating.score,  
				'result':True,
				'item_rating':Rating.item_rating(item.id)
				})
	json.dumps(context)
	return JsonResponse(context)






#Обработка страници книги 
def page(request,item_id,page_id):
	context = {}
	context.update(csrf(request))
	item = Item.objects.get(id=item_id)
	page = Item.objects.get(id=item_id).pages.get(id = page_id)
	print(item.get_first_page)
	context.update({
		'page':page,
		'item':item,
		'register_form': UserCreationForm(),
		'login_form': LoginForm(),
	})



	return render(request,"page.html",context)	



#Обработка оставления комментария 
def leave_comment(request,item_id):
	context= {}
	try:
		item = Item.objects.get(id = item_id)
	except:
		raise Http404("no item")
	comments = item.comments.filter(parent__isnull=True)
	if request.method == 'POST' and request.is_ajax():
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			parent_obj = None
			try:
				parent_id = int(request.POST.get('parent_id'))
			except:
				parent_id = None


			try:
				profile = request.user.profile
			except:
				profile = Profile()
				profile.user = request.user
				profile.username = request.user.username
				if profile:
					profile.save()


			if parent_id:
				parent_obj = Comment.objects.get(id=parent_id)
				if parent_obj:
					replay_comment = comment_form.save(commit=False)
					replay_comment.parent = parent_obj


			new_comment = comment_form.save(commit=False)
			new_comment.item = item
			new_comment.comment_author = auth.get_user(request)
			new_comment.save()
			date = new_comment.comment_date.strftime("%d %B , %Y %H:%M")


			context.update({'result':True,
							'parent':parent_id,
							'replies':new_comment.get_total_replies(),
							'comment_author_image':new_comment.comment_author.profile.image_url,
							'comment_author_id': new_comment.comment_author.profile.id,
							'comment_author':new_comment.comment_author.username,
							'comment_date': date,
							'comment_text':new_comment.comment_text,
							'comment_id':new_comment.id,
							'item_id':item_id,
							'user_id':request.user.id,
							})


			
	else:
		context.update({'result':False})
	json.dumps(context)
	return JsonResponse(context)





#Обработка добавления лайка 
def comment_add_like(request, item_id,comment_id):
	context = {}
	comment = Comment(comment_id)
	try:
		comment.likes
	except:
		Like.objects.create(comment=comment)
	if request.user.is_authenticated and request.is_ajax():

		if request.user in comment.likes.users.all():
			comment.likes.users.remove(request.user)
		else:
			comment.likes.users.add(request.user)
		context.update({'total_likes':comment.get_total_likes(), 'result':'success'})
		json.dumps(context)
		return JsonResponse(context)	
	else:
		if not  request.user.is_authenticated:

			messages.error(request,'Войдите или зрегистрируйтесь')
		json.dumps(context)
		return JsonResponse(context)	



def show_all_comments(request, item_id):
	context = {}
	context['result'] = False
	if request.is_ajax():
		item = Item.objects.get(id = item_id)

		comment_list = item.comments.filter(parent__isnull = True).order_by('-comment_date')[20:]
		for comment in comment_list:
			context.update({comment.id:{
					'parent':comment.parent_id,
					'replies':comment.get_total_replies(),
					'comment_author_image':comment.comment_author.profile.image_url,
					'comment_author_id': comment.comment_author.profile.id,
					'comment_author':comment.comment_author.username,
					'comment_date': comment.comment_date.strftime("%d %B , %Y %H:%M"),
					'comment_text':comment.comment_text,
					'item_id':item_id,
					'user_id':request.user.id,
					}
				})
			if comment.replies:
				for reply in comment.replies.all():
					context.update({reply.id:{
							'parent':reply.parent_id,
							'replies':reply.get_total_replies(),
							'comment_author_image':reply.comment_author.profile.image_url,
							'comment_author_id': reply.comment_author.profile.id,
							'comment_author':reply.comment_author.username,
							'comment_date': reply.comment_date.strftime("%d %B , %Y %H:%M"),
							'comment_text':reply.comment_text,
							'user_id':request.user.id,
							}
						})					




		context.update({'result':True})

	else:
		messages.error(request,'ajax error')
	json.dumps(context)
	return JsonResponse(context)





#Обработка изминения комментария 
def edit_comment(request,item_id):
	context = {}
	context['result'] = False
	try:
		item = Item.objects.get(id = item_id)
	except:
		return Http404
	if request.is_ajax():
		comment = item.comments.get(id = int(request.POST['comment_id']))
		comment_author_id = comment.comment_author.id
		if comment_author_id == request.user.id:
			comment.comment_text = request.POST['comment_text']
			comment.save()
			context.update({
					'comment_id':comment.id,
					'comment_text':comment.comment_text,
				})
			context['result'] = True
	json.dumps(context)
	return JsonResponse(context)















