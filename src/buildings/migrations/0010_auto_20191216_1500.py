# Generated by Django 2.2.7 on 2019-12-16 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0009_auto_20191216_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='floor',
            name='number',
            field=models.PositiveIntegerField(null=True, verbose_name='Floor number'),
        ),
    ]
