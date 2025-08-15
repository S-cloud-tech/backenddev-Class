from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(GeneralInfo)
class GeneralInfoAdmin(admin.ModelAdmin):
    list_display = [
        'site_name',
        'email',
        'location',
    ]
