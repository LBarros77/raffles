# Generated by Django 5.0.4 on 2024-05-12 23:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raffle', '0001_initial'),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CartItems',
            new_name='CartItem',
        ),
    ]