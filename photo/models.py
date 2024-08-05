from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()

def post_image_path(instance, filename):
    return f'post_images/user_{instance.user.id}/{filename}'
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/',)
    title = models.CharField(max_length=200, blank=False)
    about = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    CATEGORY_CHOICES = [
        ('phones', 'Phone'),
        ('shoes', 'Shoes'),
        ('clothes', 'Clothes'),
    ]

    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES,blank=True
    )

    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        verbose_name_plural = 'Posts'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    about = models.TextField(max_length=500, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}--{self.about}'
    class Meta:
        verbose_name_plural = 'User Profiles'