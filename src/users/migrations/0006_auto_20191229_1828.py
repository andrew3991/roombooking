# Generated by Django 2.2.6 on 2019-12-29 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20191229_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='company_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='email_domain',
        ),
    ]
