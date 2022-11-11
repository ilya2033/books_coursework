from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import os
import re




#Модель профиля 
class Profile(models.Model):
    default_img = r'.*(profile_image\.png)$'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile' )
    first_name = models.CharField(max_length = 50, blank = True)
    last_name = models.CharField(max_length = 50, blank = True)
    image = models.ImageField(upload_to='avatars',default = "avatars\\profile_image.png")
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(timezone.now,null=True, blank=True,)

    def __str__(self):
        return self.user.username
    

    #Получение пути аватарки 
    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return str(self.image.url)


    #Удаление старого изображения 
    def save_image(self, *args, **kwargs):
        try:
            this = Profile.objects.get(id=self.id)
            if this.image and not re.match(self.default_img,this.image.url) :
                this.image.delete()   
        except ObjectDoesNotExist: 
            pass        


#Генерация имени файла изображения 
def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (profile.user.id,)
    return os.path.join('uploads', filename)