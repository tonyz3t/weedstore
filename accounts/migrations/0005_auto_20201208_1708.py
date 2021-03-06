# Generated by Django 3.1.2 on 2020-12-09 01:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20201130_1608'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_on_card', models.CharField(max_length=60)),
                ('card_number', models.BigIntegerField()),
                ('exp_date', models.IntegerField(max_length=4)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='default_address',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.address'),
        ),
        migrations.AlterField(
            model_name='address',
            name='first_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='address',
            name='last_name',
            field=models.CharField(max_length=30),
        ),
    ]
