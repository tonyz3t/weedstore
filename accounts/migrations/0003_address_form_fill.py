# Generated by Django 3.1.2 on 2020-12-01 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='form_fill',
            field=models.BooleanField(default=False),
        ),
    ]