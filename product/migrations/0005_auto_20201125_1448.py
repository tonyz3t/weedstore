# Generated by Django 3.1.2 on 2020-11-25 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_image_isthumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='url',
            field=models.URLField(max_length=500),
        ),
    ]
