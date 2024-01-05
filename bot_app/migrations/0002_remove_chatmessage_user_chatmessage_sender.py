# Generated by Django 4.2.4 on 2024-01-05 12:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bot_app", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chatmessage",
            name="user",
        ),
        migrations.AddField(
            model_name="chatmessage",
            name="sender",
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
