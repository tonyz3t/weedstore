# Generated by Django 3.1.2 on 2020-12-01 00:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_address_form_fill'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='form_fill',
            new_name='default',
        ),
    ]
