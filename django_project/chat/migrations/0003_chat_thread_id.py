# Generated by Django 5.1.1 on 2024-10-04 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_rename_chats_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='thread_id',
            field=models.IntegerField(default=1),
        ),
    ]
