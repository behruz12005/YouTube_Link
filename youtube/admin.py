from django.contrib import admin

from .models import YouTobeModel,Comment

admin.site.register(YouTobeModel)
admin.site.register(Comment)