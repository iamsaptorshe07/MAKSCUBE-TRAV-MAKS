# Generated by Django 2.2 on 2020-08-28 20:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('name', models.CharField(max_length=100)),
                ('DOB', models.DateField()),
                ('phNo', models.BigIntegerField(unique=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10)),
                ('country', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=20)),
                ('zipCode', models.BigIntegerField()),
                ('address', models.CharField(max_length=100)),
                ('creationTime', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PhoneVerification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneNo', models.BigIntegerField()),
                ('verification', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_access', models.BooleanField(default=False)),
                ('agency_access', models.BooleanField(default=False)),
                ('guide_access', models.BooleanField(default=False)),
                ('uniqueId', models.CharField(max_length=10, unique=True)),
                ('security_qs', models.CharField(max_length=100, null=True)),
                ('security_ans', models.CharField(max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_access', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
