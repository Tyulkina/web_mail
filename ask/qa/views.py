from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from qa.models import Question, Answer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def test(request, *args, **kwargs):
    return HttpResponse('OK')
    

def new(request):
    questions = Question.objects.new()
    page=request.GET.get('page',1)
    limit = request.GET.get('limit',10)
    try:
        paginator = Paginator(questions, limit)
    except ValueError:
         return HttpResponseNotFound("Указан некорректный limit")       
    #возможно сюда придется добавить ограничение на значение limit=1000         
    paginator.baseurl = '/popular/?page='
    try:
    	page = paginator.page(page)
    except PageNotAnInteger:
         return HttpResponseNotFound("Указан некорректный page")
    except EmptyPage:
    	page = paginator.page(paginator.num_pages)    	
    return render(request, 'questions_list.html',{'questions':page.object_list, 'paginator':paginator, 'page':page})


def popular(request):
    questions = Question.objects.popular()
    page = request.GET.get('page',1)
    limit = request.GET.get('limit',10)
    try:
        paginator = Paginator(questions, limit)
    except ValueError:
         return HttpResponseNotFound("Указан некорректный limit")       
    #возможно сюда придется добавить ограничение на значение limit=1000         
    paginator.baseurl = '/popular/?page='
    try:
    	page = paginator.page(page)
    except PageNotAnInteger:
         return HttpResponseNotFound("Указан некорректный page")
    except EmptyPage:
    	page = paginator.page(paginator.num_pages)    	
    return render(request, 'questions_list.html',{'questions':page.object_list, 'paginator':paginator, 'page':page})
        
        
def get_question(request,num):
    try:
        question = Question.objects.get(id=num)
    except Question.DoesNotExist:
        return HttpResponseNotFound("Такого вопроса не существует")
    question.answers = Answer.objects.filter(question_id=num)    
    return render(request, 'question.html',{'question':question})
    
    
    
    
    
    
    
    
