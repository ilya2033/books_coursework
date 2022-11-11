
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db.models import Avg
from items.models import Item
# Create your models here.




class item_status(models.Model):

    class STATUS(models.TextChoices):
        WILL = "Буду читать"
        DONE = "Прочитанно"
        FROZEN = "Отложенно"
        UNKNOWN = "Неизвестно"
        DEFAULT = 'Добавить'
        WATCH = 'Читаю'

    status = models.CharField(max_length=200, choices = STATUS.choices, default = STATUS.DEFAULT )
    item = models.ForeignKey(Item, related_name= "user_status",on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='item_status',on_delete=models.CASCADE)



    def __str__(self):
        return str(self.user )+ " | " +str(self.item )



class Rating(models.Model):
    max_score = 5

    item = models.ForeignKey(Item, related_name= "user_rating",on_delete=models.CASCADE)
    user =  models.ForeignKey(User, related_name='item_rating',on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(max_score)])


    def __str__(self):
        return self.item.item_title +' | ' + str(self.score) + ' | ' + self.user.username

    def item_rating(item_id):
        this = Rating.objects.filter(item = item_id)
        if this.aggregate(Avg('score'))['score__avg']:
            return round(this.aggregate(Avg('score'))['score__avg'])
        else:
            this.aggregate(Avg('score'))['score__avg']






class Library(models.Model):
    items = models.ManyToManyField(Item,related_name="libraries")
    user = models.OneToOneField(User,on_delete = models.CASCADE,related_name = "library")




    def __str__(self):
        return str(self.user )