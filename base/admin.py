from django.contrib import admin
from .models import Profile, Contest, Prediction

admin.site.register(Profile)
admin.site.register(Contest)
admin.site.register(Prediction)