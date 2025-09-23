# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admins(models.Model):
    username = models.CharField(unique=True, max_length=255)
    password_hash = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=150)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admins'


class Books(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150, blank=True, null=True)
    isbn = models.CharField(unique=True, max_length=20, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    published_year = models.IntegerField(blank=True, null=True)
    copies_available = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'books'
