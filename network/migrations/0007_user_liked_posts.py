# Generated by Django 3.1.2 on 2020-11-06 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_auto_20201106_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='liked_posts',
            field=models.ManyToManyField(blank=True, null=True, related_name='liked', to='network.Post'),
        ),
    ]
