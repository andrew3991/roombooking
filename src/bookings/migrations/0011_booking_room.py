# Generated by Django 2.2.6 on 2020-01-03 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0014_interval_status'),
        ('bookings', '0010_remove_booking_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='buildings.Room'),
        ),
    ]
