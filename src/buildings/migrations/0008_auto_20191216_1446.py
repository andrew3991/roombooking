# Generated by Django 2.2.7 on 2019-12-16 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buildings', '0007_auto_20191216_1424'),
    ]

    operations = [
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(verbose_name='Floor number')),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buildings.Building')),
            ],
        ),
        migrations.RemoveField(
            model_name='room',
            name='building',
        ),
        migrations.AlterField(
            model_name='room',
            name='floor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='buildings.Floor'),
        ),
    ]
