from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers import TaggableManager
from smart_selects.db_fields import ChainedForeignKey



from django.conf import settings




#Модель книги 
class Item(models.Model):


    class STATUS(models.TextChoices):
        COUNTINUE = "Продолжается"
        FINISH = "Законченно"
        FROZEN = "Замороженно"
        UNKNOWN = "Неизвестно"




    item_title = models.CharField('Title', max_length = 200)
    item_other_title = models.CharField('Other_title', max_length = 200, blank=True)
    item_desc = models.TextField('Description')
    item_image = models.ImageField('Image', blank = False, null= False)
    item_title_image = models.ImageField('Title_image', blank = False, null= False )
    item_likes = models.IntegerField("Likes", default=0)
    item_date = models.DateField(default=timezone.now)
    item_status = models.CharField("status", max_length=50,default = STATUS.UNKNOWN, choices = STATUS.choices)
    author = models.CharField('author',max_length=75,blank = True)
    tags = TaggableManager()
    last_upd = models.DateTimeField()


    def __str__(self):
        return self.item_title

    #Проверка на давность
    def was_published_resently(self):
        return self.item_date >= (timezone.now - datetime.timedelata(dats = 7))






    #Получение пути к картинке 
    def get_image_url(self):
        if self.item_image and hasattr(self.item_image, 'url'):
            return self.item_image.url


    #Получение пути к титульной картинке 
    def get_title_image_url(self):
        if self.item_title_image and hasattr(self.item_title_image, 'url'):
            return self.item_title_image.url


    #Получение последней страници 
    def get_last_page(self):
        return self.pages.order_by('id').last()


    #Получение первой страници
    def get_first_page(self):
        return self.pages.order_by('id').first()

    #Количество страниц в книге
    def get_total_pages(self):
        self.pages.count()


    #Удаление страхых изображений при сохранении
    def save(self, *args, **kwargs):
        try:
            this = Item.objects.get(id=self.id)
            if this.item_image != self.item_image:
                this.item_image.delete()

            if this.item_title_image != self.item_title_image:
                this.item_title_image.delete()
        except: pass
        super(Item, self).save(*args, **kwargs)



    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"



#Модель тома 
class Volume(models.Model):
    item = models.ForeignKey(Item, on_delete = models.CASCADE,related_name='volumes',name = "item")
    title = models.CharField("title", max_length=200,)

    def __str__(self):
        return str(self.item.item_title + ' | ' + self.title )[:50]




#Модель главы
class Chapter(models.Model):
    item = models.ForeignKey(Item, on_delete = models.CASCADE,related_name='chapters', name = "item")
    volume = ChainedForeignKey(
                Volume,
                chained_field="item",
                chained_model_field="item",
                show_all=False,
                auto_choose=True,
                sort=True
            )
    number = models.IntegerField(default = 0)
    pub_date = models.DateTimeField(default=timezone.now)
    title = models.CharField("title", max_length=200) 

    #Изминение процесса сохранения экзкмпляра
    def save(self, *args, **kwargs):
        self.item.last_upd = timezone.now()
        self.item.save()
        super(Chapter, self).save(*args, **kwargs)


    def __str__(self):
        return self.title




#Модель страници
class Page(models.Model):
    item = models.ForeignKey(Item, on_delete = models.CASCADE,related_name='pages', name = "item")
    Chapter = ChainedForeignKey(
                Chapter,
                chained_field="item",
                chained_model_field="item",
                show_all=False,
                auto_choose=True,
                sort=True,
                related_name = "page",
            )


    number = models.IntegerField(default = 0)
    pub_date = models.DateTimeField(default=timezone.now)
    text = models.TextField('Text', blank = False, null= False)





    def __str__(self):
        return self.item.item_title + " | "+ str(self.number)

    #Получение следующей страници
    def get_next_page(self):
        try:
            return Page.objects.get(id = self.id + 1)
        except:
            return False


    #Получение предыдущей страници 
    def get_former_page(self):
        try:
            return Page.objects.get(id = self.id - 1)
        except:
            return False
    










#Модель коментария 
class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete = models.CASCADE,related_name='comments')
    comment_author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    comment_text = models.TextField('Text', blank = False, null= False)
    comment_date = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies',on_delete=models.CASCADE)


    #Получение количества лайков
    def get_total_likes(self):
        return self.likes.users.count()


    #Получение количества ответов
    def get_total_replies(self):
        return self.replies.count()


    def __str__(self):
        return str(self.comment_text)[:30]



#Модель лайка 
class Like(models.Model):
    comment = models.OneToOneField(Comment, related_name="likes", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='requirement_comment_likes')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.comment.comment_text)[:30]











