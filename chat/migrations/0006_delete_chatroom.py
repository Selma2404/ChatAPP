# Generated by Django 4.2.1 on 2023-05-08 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_chatroom_delete_charroom'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ChatRoom',
        ),
    ]
