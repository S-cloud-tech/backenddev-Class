from django.db import models

# Create your models here.
class GeneralInfo(models.Model):
    site_name = models.CharField(max_length=255, default="BackendDev")
    location = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=16)
    open_hours = models.CharField( null=True)
    LinkedIn_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    Instagram_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.site_name

