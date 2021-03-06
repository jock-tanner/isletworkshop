# Generated by Django 2.2.12 on 2020-04-25 00:14

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('users', '0002_user_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
            ],
            options={
                'verbose_name': 'group',
                'verbose_name_plural': 'groups',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('ru', 'Русский')], default='en', max_length=5, verbose_name='Language'),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('postal_code', models.CharField(max_length=20, verbose_name='postal code')),
                ('country', models.CharField(max_length=120, verbose_name='country')),
                ('region', models.CharField(blank=True, max_length=120, null=True, verbose_name='state or administrative region')),
                ('city', models.CharField(max_length=80, verbose_name='city or town')),
                ('street', models.CharField(blank=True, max_length=80, null=True, verbose_name='street')),
                ('building', models.CharField(blank=True, max_length=20, null=True, verbose_name='building number')),
                ('flat', models.CharField(blank=True, max_length=80, null=True, verbose_name='flat, room, office number')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'address',
                'verbose_name_plural': 'addresses',
            },
        ),
    ]
