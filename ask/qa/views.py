from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from qa.models import Question, Answer, Session
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import AskForm, AnswerForm, SignupForm, LoginForm
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import random
import string

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
    error = ''
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.cleaned_data['question']=Question.objects.get(id=num)
            answer = Answer(**form.cleaned_data)
            sessionid = request.COOKIES.get('sessionid')
            try:
                session = Session.objects.get(key=sessionid, expires__gt = datetime.now())
            except Session.DoesNotExist:
                error = u'Пожалуйста, залогиньтесь'
                #return HttpResponseRedirect('/login/')
            else:
                answer.author = session.user
                answer.save()
                url=reverse(get_question,args=[num])
                return HttpResponseRedirect(url)   
    try:
        question = Question.objects.get(id=num)
    except Question.DoesNotExist:
        return HttpResponseNotFound("Такого вопроса не существует")
    question.answers = Answer.objects.filter(question_id=num)
    form = AnswerForm(initial={'question':question})
    return render(request, 'question.html',{'question':question, 'form': form, 'error': error}) 


def add_question(request):
    error = ''
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question = Question(**form.cleaned_data)
            sessionid = request.COOKIES.get('sessionid')
            try:
                session = Session.objects.get(key=sessionid, expires__gt = datetime.now())
            except Session.DoesNotExist:
                error = u'Пожалуйста, залогиньтесь'
                #return HttpResponseRedirect('/login/')
            else:
                question.author = session.user
                question.save()
                url=reverse(get_question,args=[question.id])
                return HttpResponseRedirect(url) # URL = /question/123/
    else:
        form = AskForm()
    return render(request, 'AskForm.html', {'form': form, 'error': error}) 
    
# проверка авторизации не должна быть в контроллере
# в контроллере должно быть взаимодействие в протоколом http


def generate_session_key(user):
    session = Session()
    session.key = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
    session.user = user
    session.expires = datetime.now()+timedelta(days=5)
    session.save()
    return session.key


def do_login(login, password):
    try:
        user = User.objects.get(username=login)
    except User.DoesNotExist:
        print('нет такого пользователя')
        return None
    else:
        # хэшировать пароль
        if user.password!=password:
            print('некорректный пароль')
            return None
    return generate_session_key(user)
    
    
        
def login(request):
    error = ''
    if request.method == 'POST':
        form = LoginForm(request.POST) 
        sessionid = do_login(request.POST['username'],request.POST['password'])
        if sessionid:
            response = HttpResponseRedirect('/popular/')
            response.set_cookie('sessionid', sessionid, httponly=True,expires = datetime.now()+timedelta(days=5))
            return response
        else:
            error = u'некорректный логин или пароль'    
    else:
        form = LoginForm()
    return render(request, 'LoginForm.html', {'form': form, 'error': error}) 
    

def check_login(login):
    try:
        User.objects.get(username=login)
    except User.DoesNotExist:
        return True
    else:
        return False    
        

def signup(request):
    error = ''
    if request.method == 'POST':
        form = SignupForm(request.POST)         
        if form.is_valid():
            if check_login(form.cleaned_data['username']):
                form.cleaned_data['last_login']=datetime.now()
                user = form.save()
                sessionid = generate_session_key(user)
                response = HttpResponseRedirect('/popular/')
                response.set_cookie('sessionid', sessionid, httponly=True,expires = datetime.now()+timedelta(days=5))
                return response
            else:
                print("уже есть такой логин")
                error = u'уже есть такой логин'             
    else:
        form = SignupForm()
    return render(request, 'SignupForm.html', {'form': form, 'error': error}) 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
