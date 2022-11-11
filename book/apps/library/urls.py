from django.urls import path, include
from . import views

app_name = 'library'



#Шаблоны ссылок данного приложения 
urlpatterns = [
	path('<int:item_id>/ajax/add_status',views.ajax_add_status, name = 'add_status'),
	path('ajax/<str:status>',views.ajax_get_libliary,name = 'get_library')
]