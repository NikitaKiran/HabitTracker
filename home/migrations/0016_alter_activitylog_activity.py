# Generated by Django 3.2.6 on 2022-01-17 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_activitylog_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitylog',
            name='activity',
            field=models.CharField(max_length=50),
        ),
    ]