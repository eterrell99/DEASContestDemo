from django.db import models
from django.contrib.auth.models import User
from random import randint

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_img')
    profileSlug = models.SlugField(max_length=20, blank=True, null=True)
    def __str__(self):
        return f'{self.user.username} - Profile'

class Contest(models.Model):
    title = models.CharField(default='sample title', max_length=50, null=False)
    info = models.CharField(default='sample description', max_length=500)
    url = models.CharField(default='/sample_url', max_length=40)
    lnk = models.CharField(default='hi', max_length=1000)
    cOpen = models.DateTimeField(null=True)
    cCLose = models.DateTimeField(null=True)
    slug = models.SlugField(max_length=4000, blank=True, null=True)

    def __str__(self):
        return f'{self.title}'

class Prediction(models.Model):
    source = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE,default=0)
    temp1 = models.FloatField(max_length=3, null=False, default=00.00)
    temp2 = models.FloatField(max_length=3, null=False, default=00.00)
    coverage = models.FloatField(max_length=3, null=False, default=00.00)
    predictionSlug = models.SlugField(max_length=4000, blank=True, null=True)

    def __str__(self):
        return f'{self.contest}'
