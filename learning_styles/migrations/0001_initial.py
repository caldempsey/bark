# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-08 14:35
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LearningStyles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[django.core.validators.MaxLengthValidator(100)])),
                ('spectrum_id', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Learning Styles',
            },
        ),
        migrations.CreateModel(
            name='UserLearningStyles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('learning_style', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learning_styles.LearningStyles')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Users Learning Style',
            },
        ),
        migrations.AddField(
            model_name='learningstyles',
            name='user',
            field=models.ManyToManyField(through='learning_styles.UserLearningStyles', to=settings.AUTH_USER_MODEL),
        ),
    ]
