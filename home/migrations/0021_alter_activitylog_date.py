# Generated by Django 3.2.6 on 2022-01-20 11:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_alter_activitylog_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitylog',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
