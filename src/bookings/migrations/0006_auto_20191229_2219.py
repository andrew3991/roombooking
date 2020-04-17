# Generated by Django 2.2.6 on 2019-12-29 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0005_auto_20191228_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='check_in',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='check_out',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('Approved', 'Approved'), ('Canceled', 'Canceled'), ('Pending', 'Pending')], default='Pending', max_length=30),
        ),
    ]
