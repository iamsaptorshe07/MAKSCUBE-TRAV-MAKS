# Generated by Django 2.2 on 2020-11-23 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('touring', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='agent_approval',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='order',
            name='user_cancel',
            field=models.BooleanField(default=False),
        ),
    ]