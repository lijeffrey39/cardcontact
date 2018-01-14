# Generated by Django 2.0 on 2018-01-13 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_userprofile_shortcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='shortcode',
            field=models.CharField(blank=True, max_length=15, unique=True),
        ),
    ]
