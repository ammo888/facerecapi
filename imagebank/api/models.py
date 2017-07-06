# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        token = Token.objects.create(user=instance)


class Image(models.Model):
    owner = models.ForeignKey(
        'auth.User', related_name='images', on_delete=models.CASCADE)
    date_created = models.DateTimeField('Date Created', auto_now_add=True)
    name = models.CharField('Name', max_length=64, blank=True, default='')
    gender = models.CharField('Gender', max_length=1, choices=(
        ('M', 'Male'), ('F', 'Female')), blank=True, default='')
    image = models.FileField('Image', upload_to='images', max_length=256)
    data = models.TextField('Image data', default='data')

    class Meta:
        ordering = ('date_created',)
