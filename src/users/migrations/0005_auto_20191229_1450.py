# Generated by Django 2.2.6 on 2019-12-29 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20191228_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='companies.Company'),
        ),
        migrations.DeleteModel(
            name='Company',
        ),
    ]
