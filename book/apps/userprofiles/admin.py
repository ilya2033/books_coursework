from django.contrib import admin
from .models import Profile
# Register your models here.


#Подключение моделей в админ-панель
admin.site.register(Profile)