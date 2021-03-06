# Generated by Django 2.2.6 on 2020-01-10 14:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20191229_1828'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpgradeRequest',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('in_progress', models.BooleanField(default=False)),
                ('receiver', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,
                                                  related_name='+', to=settings.AUTH_USER_MODEL)),
                ('sender', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,
                                                related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
