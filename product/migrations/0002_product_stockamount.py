# Generated by Django 3.1.2 on 2020-11-22 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stockAmount',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
    ]
