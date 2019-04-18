from django.contrib import admin
from lbgmanager import models
# Register your models here.

admin.register(models.Member)(admin.ModelAdmin)
admin.register(models.Event)(admin.ModelAdmin)
admin.register(models.Task)(admin.ModelAdmin)