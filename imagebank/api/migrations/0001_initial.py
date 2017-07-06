# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-05 08:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('name', models.CharField(blank=True, default='', max_length=64, verbose_name='Name')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], default='', max_length=1, verbose_name='Gender')),
                ('image', models.FileField(max_length=256, upload_to='images', verbose_name='Image')),
                ('data', models.TextField(default='data', verbose_name='Image data')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('date_created',),
            },
        ),
    ]
