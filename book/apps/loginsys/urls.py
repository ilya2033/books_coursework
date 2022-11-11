from django.urls import path, include
from . import views


app_name = 'loginsys'


#Шаблоны ссылок данного приложения 
urlpatterns = [
    path('login/',views.login,name = 'login'),
	path('ajax/check_login/<str:username>',views.check_login, name = 'check_login' ),
    path('logout/',views.logout,name = 'logout'),
    path('register/',views.register,name = 'register'),
 	path('ajax/check_register/',views.check_register, name = 'check_register' ),
] 

