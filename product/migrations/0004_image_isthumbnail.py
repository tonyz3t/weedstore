# Generated by Django 3.1.2 on 2020-11-23 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20201122_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='isThumbnail',
            field=models.BooleanField(default=True),
        ),
    ]