# Generated by Django 2.0 on 2018-01-14 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20180113_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='insta',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
