from django.urls import path
from . import views



app_name = 'items'

#Шаблоны ссылок данного приложения 
urlpatterns = [
	path('',views.index, name = 'index'),
    path('<int:item_id>/',views.item, name = 'item'),
    path('<int:item_id>/<int:page_id>/',views.page, name = 'page'),
    path('<int:item_id>/leave_comment/',views.leave_comment, name = 'leave_comment'),
    path('<int:item_id>/comment_add_like/<int:comment_id>/',views.comment_add_like, name = 'comment_add_like'),
    path('<int:item_id>/ajax/show_all_comments/',views.show_all_comments, name = 'show_all_comments'),
    path('<int:item_id>/ajax/edit_comment/', views.edit_comment, name = 'edit_comment'),
    path('<int:item_id>/rating/ajax/', views.item_rating, name = "item_rating"),
]
