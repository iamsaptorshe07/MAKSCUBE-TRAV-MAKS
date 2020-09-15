from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import *
from accounts.models import *
# Create your views here.

def qnaHome(request):
    qna = Qna.objects.all().order_by('-timestamp_question')
    context = {
        'QNA':qna
    }
    return render(request,'QNA/qna_home.html',context=context)

def askQuestion(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                author = request.user
                title = request.POST.get('title')
                question_body = request.POST.get('body')
                slug = ''
                for character in title:
                    if character.isalnum():
                        slug+=character
                slug+='_asked_by_{}-{}'.format(author.name.replace(" ",""),author.id)
                question = Qna(
                    author=author,
                    title = title,
                    question_body = question_body,
                    slug=slug
                )
                question.save()
                tags = request.POST.get('tags').split(',')
                for i in tags:
                    tag = QnaTags.objects.filter(tag=i)
                    print(tag)
                    if len(tag)==0:
                        tag = QnaTags(tag=i)
                        tag.save()
                        question.tags.add(tag)
                    else:
                        tag = QnaTags.objects.get(tag=i)
                        question.tags.add(tag)
                messages.success(request,'Successfully Posted Your Question')
                return redirect('qnaHome')
            except Exception as problem:
                messages.error(request,problem)
                return redirect('qnaHome')
        else:
            return HttpResponse("404 BAD REQUEST")
    else:
        return HttpResponse("404 BAD REQUEST")




def readQna(request,slug):
    if len(Qna.objects.filter(slug=slug))>0:
        question = Qna.objects.get(slug=slug)
        answer = QnaAnswer.objects.filter(question=question)
        context = {
            'Question':question,
            'Answer':answer
            }
        return render(request,'QNA/qna_details.html',context=context)
    else:
        return HttpResponse("ERROR 404")


def deleteQuestion(request,slug):
    if len(Qna.objects.filter(slug=slug,author=request.user))>0:
        qna = Qna.objects.get(slug=slug)
        qna.delete()
        messages.success(request,'Deleted')
        return redirect('qnaHome')
    else:
        return HttpResponse("ERRO 404")


def postAnswer(request,slug):
    if request.method == 'POST':
        if len(Qna.objects.filter(slug=slug))>0:
            qna = Qna.objects.get(slug=slug)
            answer = request.POST.get('Answer')
            if answer is not None:
                if len(answer)>5:
                    if request.POST.get('parent') == "":
                        object = QnaAnswer(question=qna,user=request.user,answer=answer,parent=None)
                        object.save()
                    else:
                        get_parent_question = QnaAnswer.objects.get(id=request.POST.get('parent'))
                        object = QnaAnswer(question=qna,user=request.user,answer=answer,parent=get_parent_question)
                        object.save()
                    messages.success(request,'Successfully posted your question')
                    return redirect('/qna/question/{}'.format(qna.slug))
                else:
                    messages.error(request,'Answer length should be greater than 5')
                    return redirect('/qna/question/{}'.format(qna.slug))
            else:
                messages.error(request,"Answer should not be none")
                return redirect('/qna/question/{}'.format(qna.slug))
        else:
            return HttpResponse("BAD REQUEST")
    else:
        return HttpResponse('ERROR 404')
        


def editQuestion(request):
	return render(request,'QNA/qna_edit.html')

