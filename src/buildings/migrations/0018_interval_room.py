# Generated by Django 2.2.6 on 2020-01-13 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0017_auto_20200113_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='interval',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='buildings.Room'),
        ),
    ]
