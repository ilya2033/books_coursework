from django.contrib import admin

# Register your models here.
from .models import Item, Comment, Chapter, Volume, Like,Page





#настройки страници с комментариями 
class CommentAdmin(admin.ModelAdmin):
    list_filter = ['comment_date',]  


#Настройки страници с главами 
class ChapterAdmin(admin.ModelAdmin):
	list_filter = ['volume','item']


#Настройки страници с томами 
class VolumeAdmin(admin.ModelAdmin):
	list_filter = ['item',]


#Настройки страници со страницами
class PageAdmin(admin.ModelAdmin):
	list_filter = ['item','Chapter']



#Подключение моделей в админ-панель
admin.site.register(Item,)
admin.site.register(Like,)
admin.site.register(Page,PageAdmin)
admin.site.register(Volume,VolumeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Chapter,ChapterAdmin)
