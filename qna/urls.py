from django.urls import path
from .views import *

urlpatterns = [
    path('',qnaHome,name='qnaHome'),
    path('askQuestion',askQuestion,name='AskQuestion'),
    path('question/<str:slug>',readQna,name='fullQna'),
    path('question/delete/<str:slug>',deleteQuestion,name='deletQna'),
    path('answer/<str:slug>',postAnswer,name='postAnswer'),
	path('myquestion/edit/<str:slug>',editQuestion,name='editQuestion'),
	path('myquestion/ask/search',qnaSearch,name='qnaSearch')
    ]