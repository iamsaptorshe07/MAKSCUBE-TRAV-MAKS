from django.db import models
from accounts.models import *
# Create your models here.
class QnaTags(models.Model):
    tag = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.tag

class Qna(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    question_body = models.TextField()
    slug = models.SlugField(unique=True)
    tags = models.ManyToManyField(QnaTags,related_name='Question_Tags')
    upvote = models.ManyToManyField(User,related_name='Upvote_User',blank=True)
    timestamp_question = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class QnaAnswer(models.Model):
    question = models.ForeignKey(Qna,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    answer = models.TextField()
    parent = models.ForeignKey('self',on_delete=models.CASCADE,blank=True, null=True)
    timestamp_answer = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer