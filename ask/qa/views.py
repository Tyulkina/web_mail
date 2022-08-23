from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from qa.models import Question, Answer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import AskForm, AnswerForm
from django.urls import reverse

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
    paginator.baseurl = '/new/?page='
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
    paginator.baseurl = '/popular/?page='
    try:
    	page = paginator.page(page)
    except PageNotAnInteger:
         return HttpResponseNotFound("Указан некорректный page")
    except EmptyPage:
    	page = paginator.page(paginator.num_pages)    	
    return render(request, 'questions_list.html',{'questions':page.object_list, 'paginator':paginator, 'page':page})
        
        
def get_question(request,num):    
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.cleaned_data['question']=Question.objects.get(id=num)
            answer = form.save()
            url=reverse(get_question,args=[num])
            return HttpResponseRedirect(url)# URL = /question/123/
        else:
            print(request.POST)
            return HttpResponseNotFound("Что-то пошло не так")

    else:        
        try:
            question = Question.objects.get(id=num)
        except Question.DoesNotExist:
            return HttpResponseNotFound("Такого вопроса не существует")
        question.answers = Answer.objects.filter(question_id=num)
        form = AnswerForm(initial={'question':question})
        return render(request, 'question.html',{'question':question, 'form': form})


def add_question(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AskForm(request.POST) # bind data to a form
        if form.is_valid():
            question = form.save()
            url=reverse(get_question,args=[question.id])
            return HttpResponseRedirect(url) # URL = /question/123/

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AskForm()

    return render(request, 'AskForm.html', {'form': form}) 
    
    
    
    
