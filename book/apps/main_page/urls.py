from django.urls import path, include
from . import views


app_name = 'main_page'


#Шаблоны ссылок данного приложения 
urlpatterns = [
	path('',views.index, name = 'index'),
] 
