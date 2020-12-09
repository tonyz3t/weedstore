# Generated by Django 3.1.2 on 2020-11-14 03:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cart', '__first__'),
        ('accounts', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderJSON',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(null=True)),
                ('orderID', models.IntegerField(null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField()),
                ('isOrdered', models.BooleanField(default=False)),
                ('orderItems', models.ManyToManyField(to='cart.CartItem')),
                ('owner', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.profile')),
            ],
        ),
    ]