# Generated by Django 2.2 on 2020-11-23 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('touring', '0004_auto_20201123_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='agent_approval',
            field=models.BooleanField(default=False),
        ),
    ]