# Generated by Django 3.1.2 on 2020-11-06 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20201106_1608'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='like_count',
            new_name='like_counter',
        ),
    ]
