# Generated by Django 2.2 on 2020-12-31 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('travelagency', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TourWishList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishedTour', to='travelagency.Tour')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wisher', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
