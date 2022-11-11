from django.urls import path, include
from . import views


app_name = 'userprofiles'


#Шаблоны ссылок данного приложения 
urlpatterns = [
	path('',views.index,name = 'index'),
	path('update',views.update_profile,name = 'update'),
	path('<int:profile_id>', views.show_profile, name = "profile"),
] 

