from django.contrib import admin

from .models import Library,item_status, Rating


#Подключение моделей в админ-панель
admin.site.register(Library,)
admin.site.register(Rating,)
admin.site.register(item_status,)