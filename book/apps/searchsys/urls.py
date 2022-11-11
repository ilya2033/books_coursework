from django.urls import path,include
from django.conf.urls import *
from . import views


app_name = "searchsys"



#Шаблоны ссылок данного приложения 
urlpatterns = [
	path('',views.search_item, name="search_bar"),
	path('tag/<slug:tag>',views.tag, name = "tag_search"),
	url(r'^ajax/tag/pos=(?P<pos_tags>[\w.@+-]*),neg=(?P<neg_tags>[\w.@+-]*),order=(?P<order>[\w.@+-]*)/$',views.ajax_tag, name = "ajax_tag_search"),
	path('ajax/<data>',views.ajax_search_item, name="ajax_search_bar"),
	url(r'^ajax/tags/exclude=(?P<exclude_tags>[\w.@+-]*),(?P<data>[\w.@+-]*)/$',views.ajax_search_tag,name = "ajax_search_tag"),
]