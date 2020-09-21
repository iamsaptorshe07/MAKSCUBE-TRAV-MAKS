from django.contrib import admin
from accounts.models import *
from qna.models import *
# Register your models here.

class QnaAdmin(admin.ModelAdmin):
    model = Qna
    list_display = ('title','author','question_body','timestamp_question')
    search_fields = ['title','question_body','slug']

class AnswerAdmin(admin.ModelAdmin):
    model = QnaAnswer
    list_display = ('question','user','answer','parent','timestamp_answer')
    search_fields = ['question',]

admin.site.register(Qna,QnaAdmin)
admin.site.register(QnaTags)
admin.site.register(QnaAnswer,AnswerAdmin)