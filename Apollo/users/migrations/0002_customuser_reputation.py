# Generated by Django 4.1.2 on 2022-11-15 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='reputation',
            field=models.IntegerField(default=0, verbose_name='Reputation'),
        ),
    ]