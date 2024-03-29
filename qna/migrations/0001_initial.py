# Generated by Django 2.2 on 2020-12-31 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Qna',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('question_body', models.TextField()),
                ('slug', models.SlugField(unique=True)),
                ('timestamp_question', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QnaTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='QnaAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('timestamp_answer', models.DateTimeField(auto_now_add=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='qna.QnaAnswer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qna.Qna')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='qna',
            name='tags',
            field=models.ManyToManyField(related_name='Question_Tags', to='qna.QnaTags'),
        ),
        migrations.AddField(
            model_name='qna',
            name='upvote',
            field=models.ManyToManyField(blank=True, related_name='Upvote_User', to=settings.AUTH_USER_MODEL),
        ),
    ]
